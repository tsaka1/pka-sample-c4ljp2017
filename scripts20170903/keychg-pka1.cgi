#!/usr/local/bin/ruby
#
# An example of sign-in by public-key authentication
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

u_name = sess[USERNAME]
u_pubkey = cgi["pubkey"]
salt = nil
pass = nil
status = nil
db = SQLite3::Database.new($db_name)
begin
  begin
    db.transaction{
      db.execute("select status from pka where email = ?;",
	  u_name){ |r|
	status = r[0]
      }
    }
  rescue SQLite3::BusyException
    sleep(0.1)
    retry
  end
  if status == "valid"
    begin
      db.transaction{
	db.execute("update pka set pubkey = ? where email = ?;",
	  u_pubkey, u_name)
      }
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end
    redirect_to(cgi, $home_uri)
    log.info($0) { "reset keypair OK, redirect to #{$home_uri}" }
  else
      redirect_to(cgi, $sign_in_uri)
      log.info($0) { "#{u_name} is invalid, redirect to #{$sign_in_uri}" }
  end
ensure
  db.close
end

log.close
