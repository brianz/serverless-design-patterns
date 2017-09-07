from cupping.db import dbtransaction, commit_session, get_session

#
# def test_session_create_name_required():
#     with pytest.raises(ValueError) as e:
#         Session.create({
#                 'name': '',
#                 'formName': 'myform',
#         })
#
#
# def test_session_create_form_name_required():
#     with pytest.raises(ValueError) as e:
#         Session.create({
#                 'name': 'Session',
#                 'formName': '',
#         })
#
#
# def test_session_create_account_id_requires_int():
#     with pytest.raises(ValueError) as e:
#         Session.create({
#             'name': 'Test Session',
#             'formName': 'SCAA',
#             'accountId': 'abc123',
#             'userId': 12345
#         })
#     assert 'account_id field must be an integer value' in str(e)
#
#
# def test_session_create_user_id_requires_int():
#     with pytest.raises(ValueError) as e:
#         Session.create({
#             'name': 'Test Session',
#             'formName': 'SCAA',
#             'accountId': '123',
#             'userId': 'abc',
#         })
#     assert 'user_id field must be an integer value' in str(e)
#
#
# def test_session_create_no_cuppings():
#     s = Session.create({
#             'name': 'Test Session',
#             'formName': 'SCAA',
#     })
#     assert s.id
#     assert s.name == 'Test Session'
#     assert s.form_name == 'SCAA'
#     assert s.cuppings == []
#     assert s.account_id == None
#     assert s.user_id == None
#
#
# def test_session_create_cuppings():
#     s = Session.create({
#             'name': 'Test Session',
#             'formName': 'SCAA',
#             'cuppings': [
#                 {
#                     'scores': {'Aroma': 8, 'Flavor': 6},
#                     'overallScore': 88.8,
#                 },
#                 {
#                     'scores': {'Aroma': 6, 'Flavor': 7},
#                     'overallScore': 75,
#                 },
#             ]
#     })
#     assert s.id
#
#     expected_overall = sorted([Decimal('88.8'), Decimal('75')])
#     actual_overall = sorted([c.overall_score for c in s.cuppings])
#     assert expected_overall == actual_overall
#     assert [c.id for c in s.cuppings]
#
# def test_session_create_with_user_and_account():
#     s = Session.create({
#             'name': 'Test Session',
#             'formName': 'SCAA',
#             'accountId': '123',
#             'userId': '555000',
#     })
#     assert s.id
#     assert s.account_id == 123
#     assert s.user_id == 555000
#
