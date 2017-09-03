#!/usr/local/bin/ruby
#
# An example of sign-in by password authentication
#

require("cgi")
require("cgi/session")
require("logger")
require("sqlite3")
require("digest/sha1")

load(Dir.getwd + "/config.rb")

log = Logger.new($log_file)
log.level = Logger::INFO

cgi = CGI.new
sess = CGI::Session.new(cgi, {
  "session_secure" => true,
  "tmpdir" => $sess_dir,
  "prefix" => $sess_prefix
  })

u_name = cgi["email"]
u_pass = cgi["pwd"]
salt = nil
pass = nil
status = nil
db = SQLite3::Database.new($db_name)
begin
  begin
    db.transaction{
      db.execute("select salt, passwd, status from pwd where email = ?;",
	  u_name){ |r|
	salt = r[0]
	pass = r[1]
	status = r[2]
      }
    }
  rescue SQLite3::BusyException
    sleep(0.1)
    retry
  end
  if status == "valid"
    if Digest::SHA1.hexdigest(salt + u_pass) == pass
      sess[USERNAME] = u_name
      redirect_to(cgi, $home_uri)
      log.info($0) { "sign in OK, redirect to #{$home_uri}" }
    else
      redirect_to(cgi, $sign_in_uri)
      log.info($0) { "sign in NG, redirect to #{$sign_in_uri}" }
    end
  else
      redirect_to(cgi, $sign_in_uri)
      log.info($0) { "#{u_name} is invalid, redirect to #{$sign_in_uri}" }
  end
ensure
  db.close
end

log.close
