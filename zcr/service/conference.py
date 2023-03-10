import random
from sqlalchemy import and_

from zcr.cache.backends.redis_cache import RedisCache
from zcr.config.settings import settings
from zcr.core.celery import app
from zcr.core.log import Log, INFO
from zcr.models import ConferenceReservation, ConferenceParticipation
from zcr.view.decorators import mysql_session, timer

class ConferenceService(object):
	@staticmethod
	@mysql_session
	def fetch_by_time(session, start_time, end_time, applicant):
		session = session()
		conference = session.query(ConferenceReservation.id)		 \
							.filter(ConferenceReservation.start_time < end_time)		\
							.filter(ConferenceReservation.end_time > start_time)		\
							.filter(ConferenceReservation.applicant == applicant).first()
		return conference

	@staticmethod
	@timer
	def generate_conference_id():
		conference_id = ConferenceId().generate()
		return conference_id

	@staticmethod
	@mysql_session
	def create_reservation(session, reservation):
		session = session()
		reservation_obj = ConferenceReservation(**reservation)
		session.add(reservation_obj)
		session.commit()
		session.flush()
		reservation_id = reservation_obj.id
		return reservation_id


	@staticmethod
	@mysql_session
	def create_participation(session, participation):
		session = session()
		session.add(ConferenceParticipation(**participation))
		session.commit()

	@staticmethod
	@app.task
	@mysql_session
	def start_conference(session, conference_id):
		#Log.log_show_store(f'会议{conference_id}开始！', INFO)
		print(f'会议{conference_id}开始')
		session = session()
		session.query(ConferenceReservation) \
			.where(and_(ConferenceReservation.conference_id == conference_id, \
						ConferenceReservation.status == 0)) \
			.update({'status': 1})
		session.commit()

	@staticmethod
	@app.task
	@mysql_session
	def end_conference(session, conference_id):
		#Log.log_show_store(f'会议{conference_id}结束！', INFO)
		print(f'会议{conference_id}结束')
		session = session()
		session.query(ConferenceReservation) \
			.where(and_(ConferenceReservation.conference_id == conference_id, \
						ConferenceReservation.status == 1)) \
			.update({'status': 2})
		session.commit()

	@staticmethod
	@app.task
	@mysql_session
	def delete_conference(session, conference_id):
		session = session()
		conference = session.query(ConferenceReservation) \
			.filter(ConferenceReservation.conference_id == conference_id) 

		session.query(ConferenceParticipation) \
				.filter(ConferenceParticipation.reservation_id == \
					conference.first().id) \
				.delete()
		conference.delete()
		session.commit()

class ConferenceId(object):
	__cache = None
	__instance = None
	extra_max = 10**6-1

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			return object.__new__(cls)
		return cls.__instance

	def __init__(self):
		import inspect
		if self.__cache is None:
			self.__cache = RedisCache(settings.CACHES_CONF.default_redis)

	def generate(self):
		_id = random.randint(10**5, 9 * 10**5 - 1)
		if (self.redis_cache.call_method('sismember', 'conference_id', str(_id))): 
			self.redis_cache.call_method('sadd', 'conference_id', str(self.extra_max))
			self.extra_max -= 1
			return self.extra_max + 1
		else:
			self.redis_cache.call_method('sadd', 'conference_id', str(_id))
			return _id

	@property
	def redis_cache(self):
		return self.__cache
