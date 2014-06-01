import unittest

import angel
# Put your credentials into config.py
# in the following format
"""
CLIENT_ID = '8678157397d4e21c6c6bed7a0c0fa366'
CLIENT_SECRET = '01a0deb42173a19122291b08247f57f2'
ACCESS_TOKEN = 'b0cf040043612cc40c5e37478354ebdc'

### If you want to test your profile (test_self())
### Fill the credentials with the information
### on your angellist account

MY_NAME =
TWITTER_URL =
ONLINE_BIO_URL =
LINKEDIN_URL =
GITHUB_URL =
EMAIL =
ANGELLIST_URL =
ID =
"""

import config

MY_ID = str(config.ID)
VIACOM_ID = '40744'
WHATSAPP_ID = '78902'
UBER_ID = '19163'
AIRBNN_ID = '32677'
KARMA_ID = '29741'
CB_INSIGHTS_ID = '344401'
ANGELLIST_ID = '6702'

angel = angel.AngelList(config.CLIENT_ID,
                        config.CLIENT_SECRET,
                        config.ACCESS_TOKEN
                       )

class AngelListTestCase(unittest.TestCase):


  def set_up(self):
    pass


  def tear_down(self):
    pass


  def test_self(self):
    self_ = angel.get_self()
    assert self_['name'] == config.MY_NAME
    assert self_['twitter_url'] == config.TWITTER_URL
    assert self_['online_bio_url'] == config.ONLINE_BIO_URL
    assert self_['linkedin_url'] == config.LINKEDIN_URL
    assert self_['github_url'] == config.GITHUB_URL
    assert self_['email'] == config.EMAIL
    assert self_['angellist_url'] == config.ANGELLIST_URL
    assert int(self_['id']) == config.ID


  def test_search_for_slugs(self):
    slug_ = angel.get_search_for_slugs('karma')
    assert int(slug_['id']) == 29741
    assert slug_['name'] == 'Karma'
    assert slug_['type'] == 'Startup'
    assert slug_['url'] == 'https://angel.co/karma'


  def test_search(self):
    # Get the first item of the list
    # Check if the search of angel list actually works
    search_ = angel.get_search('cb insights')
    s_ = search_[0]
    assert type(search_) == list
    assert type(s_) == dict
    assert int(s_['id']) == 344401
    assert s_['name'] == 'CB Insights'
    assert s_['type'] == 'Startup'
    assert s_['url'] == 'https://angel.co/cb-insights-1'


  def test_users_batch(self):
    n = 30
    ids = list(map(lambda k: str(k), range(n)))
    batch_ = angel.get_users_batch(ids)
    assert len(batch_) <= n
    keys = ['facebook_url', 'bio', 'name', 'roles', 'github_url',
            'angellist_url', 'image', 'linkedin_url', 'locations', 'skills',
            'twitter_url', 'what_ive_built', 'dribbble_url', 'behance_url',\
            'blog_url', 'aboutme_url', 'follower_count', 'online_bio_url',
            'investor', 'id']
    if batch_ and len(batch_) > 0:
      assert sorted(list(batch_[0].iterkeys())) == sorted(keys)





  def test_comments(self):
    comments_ = angel.get_comments('Startup', KARMA_ID)
    assert type(comments_) == list
    assert type(comments_[0]) == dict
    assert len(comments_) > 6


  def test_jobs(self):
    # Test two pages
    for pg in [1, 2]:
      jobs_ = angel.get_jobs(page=pg)
      expected_job_keys = sorted(['per_page', 'last_page', 'total', 'jobs', 'page'])
      assert type(jobs_) == dict
      assert expected_job_keys == sorted(list(jobs_.iterkeys()))


  def test_job_by_id(self):
    j_ = angel.get_job_by_id(97)
    assert type(j_) == dict
    assert int(j_['id']) == 97
    assert j_['angellist_url'] == 'https://angel.co/jobs?startup_id=6702'
    assert j_['created_at'] == '2011-12-05T21:05:43Z'
    assert j_['currency_code'] == 'USD'
    assert float(j_['equity_cliff']) == 1.0
    assert float(j_['equity_max']) == 0.2
    assert float(j_['equity_min']) == 0.2
    assert float(j_['equity_vest']) == 6.0
    assert int(j_['salary_max']) == 150000
    assert int(j_['salary_min']) == 120000
    # Make sure that the resulting data structure is a data type
    assert type(j_['startup']) == dict


  def test_startup_jobs(self):
    jobs_ = angel.get_startup_jobs(6702)
    j_ = jobs_[0]
    assert type(j_) == dict
    assert int(j_['id']) == 97
    assert j_['angellist_url'] == 'https://angel.co/jobs?startup_id=6702'
    assert j_['created_at'] == '2011-12-05T21:05:43Z'
    assert j_['currency_code'] == 'USD'
    assert float(j_['equity_cliff']) == 1.0
    assert float(j_['equity_max']) == 0.2
    assert float(j_['equity_min']) == 0.2
    assert float(j_['equity_vest']) == 6.0
    assert int(j_['salary_max']) == 150000
    assert int(j_['salary_min']) == 120000
    # Make sure that the resulting data structure is a data type
    assert type(j_['startup']) == dict


  def test_tag_jobs(self):
    jobs_ = angel.get_tag_jobs(1692)
    assert type(jobs_) == dict
    assert type(jobs_['jobs']) == list
    expected_job_keys = sorted(['per_page', 'last_page', 'total', 'jobs', 'page'])
    assert sorted(expected_job_keys) == sorted(list(jobs_.iterkeys()))


  def test_likes(self):
    likes_ = angel.get_likes('Comment', 3800)
    expected_job_keys = sorted(['per_page', 'last_page', 'total', 'likes', 'page'])
    assert sorted(expected_job_keys) == sorted(list(likes_.iterkeys()))
    assert type(likes_['likes']) == list


  def test_messages(self):
    m_ = angel.get_messages()
    expected_message_keys = sorted(['per_page', 'last_page', 'total', 'messages', 'page'])
    assert sorted(list(m_.iterkeys())) == expected_message_keys


  def test_press(self):
    for id_ in [ANGELLIST_ID, CB_INSIGHTS_ID]:
      m_ = angel.get_press(id_)
      expected_message_keys = sorted(['per_page', 'last_page', 'total', 'press', 'page'])
      assert sorted(list(m_.iterkeys())) == expected_message_keys


  def test_press_id(self):
    expected_keys = sorted(['title', 'url', 'created_at', 'updated_at', 'id', 'snippet', 'owner_type', 'posted_at', 'owner_id'])
    p_ = angel.get_press_by_id(990)
    assert sorted(list(p_.iterkeys())) == expected_keys
    assert int(p_['id']) == 990
    assert p_['owner_id'] == 89289
    assert p_['url'] == 'http://goaleurope.com/2012/04/11/introducing-ukranian-accelerator-eastlabs-and-its-first-teams/'
    assert p_['updated_at'] == '2012-05-10T17:10:23Z'
    assert p_['created_at'] == '2012-05-10T17:10:23Z'
    assert p_['title'] == 'Startup news from Ukraine: gift selection service ActiveGift launches today'
    assert p_['snippet'] == 'Introducing Ukranian accelerator Eastlabs and its first teams'
    assert p_['posted_at'] == '2012-04-11'
    assert p_['owner_type'] == 'Startup'



if __name__ == '__main__':
  unittest.main()
