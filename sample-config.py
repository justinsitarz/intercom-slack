slack_url = ''
intercom_account_id = ''
intercom_bearer_token = ''



config = 		{	'intercom_conv_url': 	'https://api.intercom.io/conversations',
					'intercom_user_url': 	'https://api.intercom.io/users/',
					'slack_headers':		{ 'Content-type': 'application/json' },
					'slack_url':			slack_url,
					'intercom_link_url':	'https://app.intercom.io/a/apps/' + intercom_id + '/inbox/conversation/',
					'intercom_headers':		{ 'Accept': 'application/json', 'Authorization': 'Bearer ' + intercom_bearer_token },
					'wait_time': 			0
				}
