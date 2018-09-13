from json import loads
from rest_framework import status
from rest_framework.test import APITestCase
from news.models import Profile, Section
from news.tests import NUM_OBJECTS, authenticate, get_profile, get_entity


class SectionTestCase(APITestCase):
    username = None

    def setUp(self):
        authenticate(self)

        for profile in Profile.objects.all():
            for i in range(NUM_OBJECTS):
                entity = '{}{}'.format(get_entity(Section), i)
                Section.objects.create(title=entity,
                                       description='Description for {}'.format(entity),
                                       user=profile)

    def test_list_get_ok(self):
        response = self.client.get('/section/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_data = loads(response.content)
        self.assertEqual(self.__get_sections().count(), len(response_data))

    def test_list_post_ok(self):
        old_sections = self.__get_sections().count()
        response = self.client.post('/section/', {"title": "title", "description": "description"})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(old_sections + 1, self.__get_sections().count())

    def test_list_post_ok_mandatory(self):
        old_sections = self.__get_sections().count()
        response = self.client.post('/section/', {"title": "only_title"})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(old_sections + 1, self.__get_sections().count())

    def test_list_post_ok_user(self):
        user_id = get_profile(self).id + 1
        response = self.client.post('/section/', {"title": "title_user", "user": user_id})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_list_post_ko_json(self):
        response = self.client.post('/section/', {"description": "only_description"})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_detail_get_ok(self):
        section = self.__get_sections().first()
        response = self.client.get('/section/{}/'.format(section.id))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_data = loads(response.content)
        self.assertEqual(section.title, response_data['title'])

    def test_detail_get_ko_user(self):
        section_id = self.__get_sections().first().id + 3
        response = self.client.get('/section/{}/'.format(section_id))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_detail_put_ok(self):
        title = "other_title"
        section = self.__get_sections().first()
        response = self.client.put('/section/{}/'.format(section.id), {"title": title})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(title, Section.objects.get(id=section.id).title)

    def test_detail_put_ko_json(self):
        section = self.__get_sections().first()
        response = self.client.put('/section/{}/'.format(section.id), {"description": "other_description"})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_detail_put_ko_user(self):
        section_id = self.__get_sections().first().id + 3
        response = self.client.put('/section/{}/'.format(section_id), {"title": "other_title"})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_detail_delete_ok(self):
        section_id = self.__get_sections().first().id
        response = self.client.delete('/section/{}/'.format(section_id))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Section.objects.filter(id=section_id).exists())

    def test_detail_delete_ko_user(self):
        section_id = self.__get_sections().first().id + 3
        response = self.client.delete('/section/{}/'.format(section_id))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def __get_sections(self):
        return Section.objects.filter(user__user__username=self.username)
