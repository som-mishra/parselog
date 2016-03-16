import datetime
import unittest
import re
import parse_test_results_with_argparse

class TestParseTestResults(unittest.TestCase):

	def setUp(self):
		self.content1 = [
			"2016-03-07 23:08:31.706 27883 DEBUG ironic.cmd.conductor [-] Configuration: main /opt/stack/old/ironic/ironic/cmd/conductor.py:43",
			"2016-03-07 23:08:31.750 27883 DEBUG ironic.cmd.conductor [-] ******************************************************************************** log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2320",
			"2016-03-07 23:08:33.707 27883 DEBUG ironic.cmd.conductor [-] Configuration options gathered from: log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2321",
			"2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322",
			"2016-03-07 23:08:36.707 27883 DEBUG ironic.cmd.conductor [-] config files: ['/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2323",
			"2016-03-07 23:08:40.707 27883 DEBUG ironic.cmd.conductor [-] ================================================================================ log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2324",
			"2016-03-07 23:08:41.707 27883 DEBUG ironic.cmd.conductor [-] bindir                         = /opt/stack/old/ironic/ironic/bin log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 23:08:43.707 27883 DEBUG ironic.cmd.conductor [-] config_dir                     = None log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 23:08:45.708 27883 DEBUG ironic.cmd.conductor [-] config_file                    = ['/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 23:08:46.708 27883 DEBUG ironic.cmd.conductor [-] control_exchange               = ironic log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 23:08:50.708 27883 DEBUG ironic.cmd.conductor [-] debug                          = True log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333"
			]

		self.content2 = [
			"++ [[ -n '' ]]",
			"++ echo 27883",
			"++ setsid /usr/local/bin/ironic-conductor --config-file=/etc/ironic/ironic.conf",
			"++ exit 0",
			"2016-03-07 23:08:31.706 27883 DEBUG ironic.cmd.conductor [-] Configuration: main /opt/stack/old/ironic/ironic/cmd/conductor.py:43",
			"2016-03-07 23:08:31.750 27883 DEBUG ironic.cmd.conductor [-] ******************************************************************************** log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2320",
			"2016-03-07 23:08:33.707 27883 DEBUG ironic.cmd.conductor [-] Configuration options gathered from: log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2321",
			"2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322",
			"2016-03-07 23:08:36.707 27883 DEBUG ironic.cmd.conductor [-] config files: ['/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2323",
			"++ setsid /usr/local/bin/ironic-conductor --config-file=/etc/ironic/ironic.conf",
			"2016-03-07 23:08:40.707 27883 DEBUG ironic.cmd.conductor [-] ================================================================================ log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2324",
			"2016-03-07 23:08:41.707 27883 DEBUG ironic.cmd.conductor [-] bindir                         = /opt/stack/old/ironic/ironic/bin log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 23:08:43.707 27883 DEBUG ironic.cmd.conductor [-] config_dir                     = None log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"++ [[ -n '' ]]",
			"++ echo 27883",	
			"2016-03-07 23:08:45.708 27883 DEBUG ironic.cmd.conductor [-] config_file                    = ['/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 23:08:46.708 27883 hello ironic.cmd.conductor [-] control_exchange               = ironic log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 23:08:50.708 27883 DEBUG ironic.cmd.conductor [-] debug                          = True log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333"
		]
		self.content3 = [
			"++ [[ -n '' ]]",
			"++ echo 27883",
			"++ setsid /usr/local/bin/ironic-conductor --config-file=/etc/ironic/ironic.conf",
			"++ exit 0",
			"2016-03-07 13:08:03.069 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] log_date_format                = %Y-%m-%d %H:%M:%S log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 13:08:03.069 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] log_dir                        = None log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 13:09:03.069 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] log_file                       = None log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"alsbnofuabwpoeifa junk junk",
			"++ setsid /usr/local/bin/ironic-conductor --config-file=/etc/ironic/ironic.conf",
			"++ exit 0",
			"2016-03-07 14:09:03.069 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] log_format                     = None log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 14:09:03.069 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] log_options                    = True log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"hellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohello :)",
			"2016-03-07 14:10:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_context_format_string  = %(asctime)s.%(msecs)03d %(levelname)s %(name)s [%(request_id)s %(user_name)s %(project_name)s] %(instance)s%(message)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 14:10:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_debug_format_suffix    = %(funcName)s %(pathname)s:%(lineno)d log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"random line",
			"2016-03-07 14:11:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_default_format_string  = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 15:08:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_exception_prefix       = %(asctime)s.%(msecs)03d %(process)d ERROR %(name)s %(instance)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 15:08:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_user_identity_format   = %(user)s %(tenant)s %(domain)s %(user_domain)s %(project_domain)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
			"2016-03-07 15:08:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] max_age                        = 0 log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333"
			]



	# test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."

	# test_line2 = "2015-10-15 15:10:34.234 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."

	# test_line3 = "1823-12-30 10:01:43.983 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."

#	def test_process_all_input_files():
#		process_all_input_files()

#	def test_get_all_input_files():
#		get_all_input_files()

#	def test_validate_args():
#		validate_args()

	def test_get_line_datetime_valid1(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual(datetime.datetime(2016, 3, 7, 23, 8, 2, 956000), parse_test_results_with_argparse.get_line_datetime(test_line1))

	def test_get_line_datetime_valid2(self):
		test_line2 = "2015-10-15 15:10:34.234 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual(datetime.datetime(2015, 10, 15, 15, 10, 34, 234000), parse_test_results_with_argparse.get_line_datetime(test_line2))

	def test_get_line_datetime_valid3(self):
		test_line3 = "1823-12-30 10:01:43.983 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual(datetime.datetime(1823, 12, 30, 10, 1, 43, 983000), parse_test_results_with_argparse.get_line_datetime(test_line3))

	def test_get_line_datetime_nodate(self):
		# Has no date
		self.assertEqual(None, parse_test_results_with_argparse.get_line_datetime("No date here"))

	def test_get_line_datetime_invaliddate(self):
		# Invalid day of month
		self.assertEqual(None, parse_test_results_with_argparse.get_line_datetime("2016-02-31 16:37:55.123 Feb. does not more than 29"))

	def test_get_line_datetime_invalidtime1(self):
		# Invalid hour for time
		self.assertEqual(None, parse_test_results_with_argparse.get_line_datetime("2016-02-28 25:37:55.123 Invalid time"))

	def test_get_line_datetime_invalidtime2(self):
		# Does not contain HH:MM:SS.SSS, missing hour/minute
		self.assertEqual(None, parse_test_results_with_argparse.get_line_datetime("2016-02-28 16:55.123 Invalid time"))

	def test_get_line_datetime_invalidtime3(self):
		self.assertEqual(None, parse_test_results_with_argparse.get_line_datetime("No date or time given"))

# 8




	# test_path1 = "/cygdrive/c/Users/shataman/Documents/grenadelogparsingstuff/"
	# test_path2 = "/cygdrive/c/Users/shataman/Documents/random/textfiles/"
	# test_path3 = "/cygdrive/c/Users/shataman/Downloads/"
	# test_path4 = "/cygdrive/c/Users/shataman/Desktop/"
	# test_path5 = "/"
	# test_path6 = "/../../cygdrive/c/Users/shataman/Downloads/"


	# all_documents1 = ["screen-ir-cond.txt", "screen-ir-cond.txt.gz", "screen-n-cond.txt", "screen-n-cond.txt.gz", "test1.txt", "test2.txt"]
	# all_documents2 = ["screen-ir-cond.txt.gz", "screen-n-cond.txt.gz"]
	# all_documents3 = ["Darwin.txt", "parkingticketcontest.txt"]
	# all_documents4 = []
	# all_documents5 = []
	# all_documents6 = ["Darwin.txt", "parkingticketcontest.txt"]


	def test_get_all_input_files1(self):
		# TODO: need to use the 'mock' library to test this function. For future, don't do at this time.
		test_path1 = "/cygdrive/c/Users/shataman/Documents/grenadelogparsingstuff/"
		all_documents1 = ["screen-ir-cond.txt", "screen-ir-cond.txt.gz", "screen-n-cond.txt", "screen-n-cond.txt.gz", "test1.txt", "test2.txt"]
		self.assertEqual(all_documents1, parse_test_results_with_argparse.get_all_input_files(test_path1))

	def test_get_all_input_files2(self):
		test_path2 = "/cygdrive/c/Users/shataman/Documents/random/textfiles/"
		all_documents2 = ["screen-ir-cond.txt.gz", "screen-n-cond.txt.gz"]
		self.assertEqual(all_documents2, parse_test_results_with_argparse.get_all_input_files(test_path2))

	def test_get_all_input_files3(self):
		test_path3 = "/cygdrive/c/Users/shataman/Downloads/"
		all_documents3 = ["Darwin.txt", "parkingticketcontest.txt"]
		self.assertEqual(all_documents3, parse_test_results_with_argparse.get_all_input_files(test_path3))

	def test_get_all_input_files4(self):
		test_path4 = "/cygdrive/c/Users/shataman/Desktop/"
		all_documents4 = []
		self.assertEqual(all_documents4, parse_test_results_with_argparse.get_all_input_files(test_path4))

	def test_get_all_input_files5(self):
		test_path5 = "/"
		all_documents5 = []
		self.assertEqual(all_documents5, parse_test_results_with_argparse.get_all_input_files(test_path5))

	def test_get_all_input_files6(self):
		test_path6 = "/../../cygdrive/c/Users/shataman/Downloads/"
		all_documents6 = ["Darwin.txt", "parkingticketcontest.txt"]
		self.assertEqual(all_documents6, parse_test_results_with_argparse.get_all_input_files(test_path6))

# 6



	
 	def test_process_file2_basic(self):
		date1 = "2016-03-07"
		time1 = "23:08:43.700"
		string1 = "DEBUG"
 		expected = self.content1[7:]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content1, mydate=date1, mytime=time1, mystring=string1))



 	def test_process_file2_no_string(self):
		date1 = "2016-03-07"
		time1 = "23:08:43.700"
 		expected = self.content1[7:]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content1, mydate=date1, mytime=time1))

 	def test_process_file2_partial_time1(self):
		date1 = "2016-03-07"
		time1 = "23:08:43"
		# JLV: Why 'if time1'
		if time1:
			timeparts = time1.split(':')
	        if len(timeparts) == 3:
	            if (re.search('\.', timeparts[2])):
	                pass
	            else:
	                time1 = time1 + '.000'
	        elif len(timeparts) == 2:
			    time1 = time1 + ':00.000'
	        elif len(timeparts) == 1:
	            time1 = time1 + ':00:00.000'
	   	else:
	   		args.TIME = "00:00:00.001"
 		expected = self.content1[7:]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content1, mydate=date1, mytime=time1))


 	def test_process_file2_partial_time2(self):
		date1 = "2016-03-07"
		time1 = "23:08"
		# JLV: Why 'if time1'
		if time1:
			timeparts = time1.split(':')
	        if len(timeparts) == 3:
	            if (re.search('\.', timeparts[2])):
	                pass
	            else:
	                time1 = time1 + '.000'
	        elif len(timeparts) == 2:
			    time1 = time1 + ':00.000'
	        elif len(timeparts) == 1:
	            time1 = time1 + ':00:00.000'
		else:
			time1 = "00:00:00.001"
 		expected = self.content1[:]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content1, mydate=date1, mytime=time1))


 	def test_process_file2_no_time(self):
		date1 = "2016-03-07"
		#time1 = None
		# if time1 is not None:
		# 	timeparts = time1.split(':')
	 #        if len(timeparts) == 3:
	 #            if (re.search('\.', timeparts[2])):
	 #                pass
	 #            else:
	 #                time1 = time1 + '.000'
	 #        elif len(timeparts) == 2:
		# 	    time1 = time1 + ':00.000'
	 #        elif len(timeparts) == 1:
	 #            time1 = time1 + ':00:00.000'
		# else:
		time1 = '00:00:00.001'
 		expected = self.content1
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content1, mydate=date1, mytime=time1))






	

 	def test_process_file2_random_lines1(self):
		date1 = "2016-03-07"
		time1 = "23:08:35"
		# string1 = "--config"
		if time1:
			timeparts = time1.split(':')
	        if len(timeparts) == 3:
	            if (re.search('\.', timeparts[2])):
	                pass
	            else:
	                time1 = time1 + '.000'
	        elif len(timeparts) == 2:
			    time1 = time1 + ':00.000'
	        elif len(timeparts) == 1:
	            time1 = time1 + ':00:00.000'
		else:
			time1 = "00:00:00.001"
 		# expected = ["2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322"
 							# "++ setsid /usr/local/bin/ironic-conductor --config-file=/etc/ironic/ironic.conf"
				# ]
		expected = self.content2[7:]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content2, mydate=date1, mytime=time1))

 	def test_process_file2_random_lines2(self):
		date1 = "2016-03-07"
		time1 = "23:08"
		string1 = "command line args"
		# JLV: Why 'if time1'
		if time1:
			timeparts = time1.split(':')
	        if len(timeparts) == 3:
	            if (re.search('\.', timeparts[2])):
	                pass
	            else:
	                time1 = time1 + '.000'
	        elif len(timeparts) == 2:
			    time1 = time1 + ':00.000'
	        elif len(timeparts) == 1:
	            time1 = time1 + ':00:00.000'
		else:
			time1 = "00:00:00.001"
 		expected = ["2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322"]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content2, mydate=date1, mytime=time1, mystring=string1))

 	def test_process_file2_random_lines3(self):
		date1 = "2016-03-07"
		time1 = "23:08"
		string1 = "hello"
		# JLV: Why 'if time1'
		if time1:
			timeparts = time1.split(':')
	        if len(timeparts) == 3:
	            if (re.search('\.', timeparts[2])):
	                pass
	            else:
	                time1 = time1 + '.000'
	        elif len(timeparts) == 2:
			    time1 = time1 + ':00.000'
	        elif len(timeparts) == 1:
	            time1 = time1 + ':00:00.000'
		else:
			time1 = "00:00:00.001"
 		expected = ["2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322",
					"2016-03-07 23:08:46.708 27883 hello ironic.cmd.conductor [-] control_exchange               = ironic log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
				]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content2, mydate=date1, mytime=time1, mystring=string1))

 	def test_process_file2_random_lines4(self):
		date1 = "2016-03-07"
		time1 = "23:08:35"
		if time1:
			timeparts = time1.split(':')
	        if len(timeparts) == 3:
	            if (re.search('\.', timeparts[2])):
	                pass
	            else:
	                time1 = time1 + '.000'
	        elif len(timeparts) == 2:
			    time1 = time1 + ':00.000'
	        elif len(timeparts) == 1:
	            time1 = time1 + ':00:00.000'
		else:
			time1 = "00:00:00.001"
 		expected = self.content2[7:]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content2, mydate=date1, mytime=time1))


 	def test_process_file2_random_lines5(self):
		date1 = "2016-03-07"
		time1 = "23:08:35"
		string1 = "--config"
		if time1:
			timeparts = time1.split(':')
	        if len(timeparts) == 3:
	            if (re.search('\.', timeparts[2])):
	                pass
	            else:
	                time1 = time1 + '.000'
	        elif len(timeparts) == 2:
			    time1 = time1 + ':00.000'
	        elif len(timeparts) == 1:
	            time1 = time1 + ':00:00.000'
		else:
			time1 = "00:00:00.001"
 		expected = ["2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322",
 					"++ setsid /usr/local/bin/ironic-conductor --config-file=/etc/ironic/ironic.conf",
				]
 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content2, mydate=date1, mytime=time1, mystring=string1))





	def test_process_file2_more1(self):
			date1 = "2016-03-07"
			time1 = "14"
			# JLV: Why 'if time1'
			if time1:
				timeparts = time1.split(':')
		        if len(timeparts) == 3:
		            if (re.search('\.', timeparts[2])):
		                pass
		            else:
		                time1 = time1 + '.000'
		        elif len(timeparts) == 2:
				    time1 = time1 + ':00.000'
		        elif len(timeparts) == 1:
		            time1 = time1 + ':00:00.000'
			else:
				time1 = "00:00:00.001"
	 		expected = self.content3[10:]
	 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content3, mydate=date1, mytime=time1))


	def test_process_file2_more2(self):
			date1 = "2016-03-07"
			time1 = "14"
			string1 = "req-a17d69b8-066c-4482-a865"
			# JLV: Why 'if time1'
			if time1:
				timeparts = time1.split(':')
		        if len(timeparts) == 3:
		            if (re.search('\.', timeparts[2])):
		                pass
		            else:
		                time1 = time1 + '.000'
		        elif len(timeparts) == 2:
				    time1 = time1 + ':00.000'
		        elif len(timeparts) == 1:
		            time1 = time1 + ':00:00.000'
			else:
				time1 = "00:00:00.001"
			# JLV: Make this a subset of self.content3.  e.g expected = self.content3[4:6] + self.content3[9:]
	 		expected = [
			 		"2016-03-07 14:09:03.069 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] log_format                     = None log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
					"2016-03-07 14:09:03.069 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] log_options                    = True log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
					"2016-03-07 14:10:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_context_format_string  = %(asctime)s.%(msecs)03d %(levelname)s %(name)s [%(request_id)s %(user_name)s %(project_name)s] %(instance)s%(message)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
					"2016-03-07 14:10:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_debug_format_suffix    = %(funcName)s %(pathname)s:%(lineno)d log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
					"2016-03-07 14:11:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_default_format_string  = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
					"2016-03-07 15:08:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_exception_prefix       = %(asctime)s.%(msecs)03d %(process)d ERROR %(name)s %(instance)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
					"2016-03-07 15:08:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] logging_user_identity_format   = %(user)s %(tenant)s %(domain)s %(user_domain)s %(project_domain)s log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
					"2016-03-07 15:08:03.070 DEBUG oslo_service.service [req-a17d69b8-066c-4482-a865-4347872504af None None] max_age                        = 0 log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333"
						]
	 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content3, mydate=date1, mytime=time1, mystring=string1))


	def test_process_file2_more3(self):
			date1 = "2016-03-07"
			time1 = "14"
			# JLV: Why 'if time1'?
			if time1:
				timeparts = time1.split(':')
		        if len(timeparts) == 3:
		            if (re.search('\.', timeparts[2])):
		                pass
		            else:
		                time1 = time1 + '.000'
		        elif len(timeparts) == 2:
				    time1 = time1 + ':00.000'
		        elif len(timeparts) == 1:
		            time1 = time1 + ':00:00.000'
			else:
				time1 = "00:00:00.001"
	 		expected = self.content3[10:]
	 		time1 = "14:00:00.000"
	 		self.assertEqual(expected, parse_test_results_with_argparse.process_file2(self.content3, mydate=date1, mytime=time1))


if __name__ == '__main__':
	unittest.main()






#print(findLines.get_date_time(test_line))

