from datetime import datetime

from zcr.core.handler import BaseHandler
from zcr.core.status import Code, Message
from zcr.service.conference import ConferenceService
from zcr.view.decorators import jwt_auth, Route
from zcr.util.datetime import datetime_to_eta

@Route(r'/conference/reserve/?')
class ReserveHandler(BaseHandler):
	@jwt_auth
	async def post(self):
		start_time = self.get_argument('start_time')
		end_time = self.get_argument('end_time')
		conference = ConferenceService.fetch_by_time(start_time, end_time,
													 self.current_user)
		if conference:
			self.write_fail(Code.Conference.PRIOD_EXIST,
							Message.Conference.PRIOD_EXIST)
		else:
			conference_id = ConferenceService.generate_conference_id()
			reservation = {
				'conference_id': conference_id,
				'applicant': self.current_user,
				'start_time': start_time,
				'end_time': end_time,
				'status': 0,
				'created_at': datetime.now(),
			}
			reservation_id = ConferenceService.create_reservation(reservation)

			participation = {
				'reservation_id': reservation_id,
				'participant': self.current_user,
				'created_at': datetime.now(),
			}
			ConferenceService.create_participation(participation)
			
			start_time = datetime_to_eta(start_time)
			end_time = datetime_to_eta(end_time)

			ConferenceService.start_conference.apply_async((conference_id, ),\
														   eta=start_time, \
														   utc=False)

			ConferenceService.end_conference.apply_async((conference_id, ), \
														 eta=end_time,	  \
														 utc=False)

			participate_url = f'/conference/particate/?conference_id={conference_id}'
			self.write_success(data={'conference_id': conference_id, \
									 'applicant': self.current_user, \
									 'participate_url': participate_url})

	@jwt_auth
	async def delete(self):
		conference_id = self.get_argument('conference_id')
		ConferenceService.delete_conference(conference_id)
		self.write_success()
