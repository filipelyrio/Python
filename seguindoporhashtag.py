from instapy import InstaPy
from instapy import smart_run

session = InstaPy(username='decoladestinos', password='Cacau.07',
headless_browser=False,
want_check_browser=False)

with smart_run(session):
	session.set_do_follow(enabled = True, percentage = 100)
	session.set_do_like(enabled = True, percentage= 100)

	session.like_by_tags(['CVCviagens', 'CVC', 'CVCBahia', 
	'agenciadeviagens', 'Turismo', 'Viagens', 'Aereo', 'ViagensAereas',
	'Viajar'], amount=5)

	comentarios = ['\U0001F44D', '\U0001F642', ':)', '\U0001F60A',
	'\U0001F60E', 'Bom', 'Legal!', '\U0001F4AF', '\U0001F44F', 
	'\U0001F4F8', 'Gostei', 'Muito bom', 'Uau']
	session.set_do_comment(enabled=True, percentage=30)
	session.set_comments(comentarios, media= 'Photo')
	session.join_pods()
