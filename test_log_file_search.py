#!/usr/bin/python

import datetime
import re
import unittest

import log_file_search

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


	def test_get_line_datetime_valid1(self):
		test_line1 = "2016-03-07 23:08:02.956 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual(datetime.datetime(2016, 3, 7, 23, 8, 2, 956000), log_file_search.get_line_datetime(test_line1))

	def test_get_line_datetime_valid2(self):
		test_line2 = "2015-10-15 15:10:34.234 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual(datetime.datetime(2015, 10, 15, 15, 10, 34, 234000), log_file_search.get_line_datetime(test_line2))

	def test_get_line_datetime_valid3(self):
		test_line3 = "1823-12-30 10:01:43.983 26887 WARNING oslo_reports.guru_meditation_report [-] Guru mediation now registers SIGUSR1 and SIGUSR2 by default for backward compatibility. SIGUSR1 will no longer be registered in a future release, so please use SIGUSR2 to generate reports."
		self.assertEqual(datetime.datetime(1823, 12, 30, 10, 1, 43, 983000), log_file_search.get_line_datetime(test_line3))

	def test_get_line_datetime_nodate(self):
		# Has no date
		self.assertEqual(None, log_file_search.get_line_datetime("No date here"))

	def test_get_line_datetime_invaliddate(self):
		# Invalid day of month
		self.assertEqual(None, log_file_search.get_line_datetime("2016-02-31 16:37:55.123 Feb. does not more than 29"))

	def test_get_line_datetime_invalidtime1(self):
		# Invalid hour for time
		self.assertEqual(None, log_file_search.get_line_datetime("2016-02-28 25:37:55.123 Invalid time"))

	def test_get_line_datetime_invalidtime2(self):
		# Does not contain HH:MM:SS.SSS, missing hour/minute
		self.assertEqual(None, log_file_search.get_line_datetime("2016-02-28 16:55.123 Invalid time"))

	def test_get_line_datetime_invalidtime3(self):
		self.assertEqual(None, log_file_search.get_line_datetime("No date or time given"))






	# Basic test with all parameters and all parts specified
 	def test_process_file2_basic(self):
		date1 = "2016-03-07"
		time1 = "23:08:43.700"
		string1 = "DEBUG"
 		expected = self.content1[7:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content1, mydate=date1, mytime=time1, mystring=string1))


 	# All time parts specified, but no string
 	def test_process_file2_no_string(self):
		date1 = "2016-03-07"
		time1 = "23:08:43.700"
 		expected = self.content1[7:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content1, mydate=date1, mytime=time1))

 	# No milliseconds and no string
 	def test_process_file2_partial_time1(self):
		date1 = "2016-03-07"
		time1 = "23:08:43"
		time1 = time1 + '.000'

 		expected = self.content1[7:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content1, mydate=date1, mytime=time1))

 	# No seconds or milliseconds, and no string
 	def test_process_file2_partial_time2(self):
		date1 = "2016-03-07"
		time1 = "23:08"
		time1 = time1 + ':00.000'

 		expected = self.content1[:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content1, mydate=date1, mytime=time1))


 	# Only date is specified, nothing else
 	def test_process_file2_no_time(self):
		date1 = "2016-03-07"

		time1 = '00:00:00.001'
 		expected = self.content1[:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content1, mydate=date1, mytime=time1))









	
 	# No string specified with content that has non-date/time lines in between
 	def test_process_file2_random_lines1(self):
		date1 = "2016-03-07"
		time1 = "23:08:35"
		time1 = time1 + '.000'

		expected = self.content2[7:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content2, mydate=date1, mytime=time1))

 	# String specified with content that has non-date/time lines in between
 	def test_process_file2_random_lines2(self):
		date1 = "2016-03-07"
		time1 = "23:08"
		time1 = time1 + ':00.000'
		string1 = "command line args"
		expected = []

		expected.append(self.content2[7])
 		self.assertEqual(expected, log_file_search.process_file2(self.content2, mydate=date1, mytime=time1, mystring=string1))


 	# Couple of the lines modified with my own search string
 	def test_process_file2_random_lines3(self):
		date1 = "2016-03-07"
		time1 = "23:08"
		time1 = time1 + ':00.000'
		string1 = "hello"
		expected = []

 		expected = ["2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322",
					"2016-03-07 23:08:46.708 27883 hello ironic.cmd.conductor [-] control_exchange               = ironic log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2333",
				]
 		self.assertEqual(expected, log_file_search.process_file2(self.content2, mydate=date1, mytime=time1, mystring=string1))


 	# No string specified and content that has non-date/time lines in between
 	def test_process_file2_random_lines4(self):
		date1 = "2016-03-07"
		time1 = "23:08:35"
		time1 = time1 + '.000'

 		expected = self.content2[7:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content2, mydate=date1, mytime=time1))


 	# Search string specified is present in both a date/time line and a line with no date/time
 	def test_process_file2_random_lines5(self):
		date1 = "2016-03-07"
		time1 = "23:08:35"
		time1 = time1 + '.000'
		string1 = "--config"

 		expected = ["2016-03-07 23:08:35.707 27883 hello ironic.cmd.conductor [-] command line args: ['--config-file=/etc/ironic/ironic.conf'] log_opt_values /usr/local/lib/python2.7/dist-packages/oslo_config/cfg.py:2322",
 					"++ setsid /usr/local/bin/ironic-conductor --config-file=/etc/ironic/ironic.conf",
				]
 		self.assertEqual(expected, log_file_search.process_file2(self.content2, mydate=date1, mytime=time1, mystring=string1))




 	# Content with non-date/time lines in between, and only the hour is specified in the time
	def test_process_file2_more1(self):
			date1 = "2016-03-07"
			time1 = "14"
			time1 = time1 + ':00:00.000'

	 		expected = self.content3[10:]
	 		self.assertEqual(expected, log_file_search.process_file2(self.content3, mydate=date1, mytime=time1))


	# Search string is req number with non-date/time lines in between in the content, and only hour is specified
	def test_process_file2_more2(self):
		date1 = "2016-03-07"
		time1 = "14"
		time1 = time1 + ':00:00.000'
		string1 = "req-a17d69b8-066c-4482-a865"

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
 		self.assertEqual(expected, log_file_search.process_file2(self.content3, mydate=date1, mytime=time1, mystring=string1))


 	# Only hour is specified in time
	def test_process_file2_more3(self):
		date1 = "2016-03-07"
		time1 = "14"
		time1 = time1 + ':00:00.000'

 		expected = self.content3[10:]
 		self.assertEqual(expected, log_file_search.process_file2(self.content3, mydate=date1, mytime=time1))







 	# Full date and full time
	def test_validate_inputs1(self):
	 	date1 = "2000-01-25"
	 	time1 = "23:34:12.123"
	 	expected = ("2000-01-25", "23:34:12.123")
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))

	# Msec missing
	def test_validate_inputs2(self):
	 	date1 = "2000-01-25"
	 	time1 = "23:34:12"
	 	expected = ("2000-01-25", "23:34:12.000")
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))

	# Sec and msec missing
	def test_validate_inputs3(self):
	 	date1 = "2000-01-25"
	 	time1 = "23:34"
	 	expected = ("2000-01-25", "23:34:00.000")
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))

	# Mins, sec, and msec are missing
	def test_validate_inputs4(self):
	 	date1 = "2000-01-25"
	 	time1 = "23"
	 	expected = ("2000-01-25", "23:00:00.000")
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))

	# Partial date and time
	def test_validate_inputs5(self):
	 	date1 = "2000-01"
	 	time1 = "23"
	 	expected = ("2000-01-01", "23:00:00.000")
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))
	
	# Only year in date, and only hour in time
	def test_validate_inputs6(self):
	 	date1 = "2000"
	 	time1 = "23"
	 	expected = ("2000-01-01", "23:00:00.000")
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))

	# Empty string for time
	def test_validate_inputs7(self):
	 	date1 = "2000-01-25"
	 	time1 = ""
	 	expected = ("2000-01-25", "00:00:00.001")
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))

	# Random string for date
	def test_validate_inputs8(self):
	 	date1 = "hello"
	 	time1 = "23"
	 	expected = None, "23:00:00.000"
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))
	
	# Random string for time
	def test_validate_inputs9(self):
	 	date1 = "2000-01-25"
	 	time1 = "blah"
	 	expected = "2000-01-25", None
	 	self.assertEqual(expected, log_file_search.validate_inputs(date1, time1))



if __name__ == '__main__':
	unittest.main()







