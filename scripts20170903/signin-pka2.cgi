#!/usr/local/bin/ruby
#
# An example of sign-in by public-key authentication
#

require("cgi")
require("cgi/session")
require("logger")
require("sqlite3")
require("openssl")

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
u_sign = cgi["sign"]
challenge = nil
pubpem = nil
status = nil
db = SQLite3::Database.new($db_name)
begin
  begin
    db.transaction{
      db.execute("select salt, pubkey, status from pka where email = ?;",
	  u_name){ |r|
	challenge = r[0]
	pubpem = r[1]
	status = r[2]
      }
    }
  rescue SQLite3::BusyException
    sleep(0.1)
    retry
  end
  if status == "valid"
    pubkey = OpenSSL::PKey::RSA.new(pubpem)
    sign = u_sign.gsub(/[0-9A-F][0-9A-F]/i){ | p | p.hex.chr }
    if pubkey.verify("sha256", sign, challenge)
      sess[USERNAME] = u_name
      begin
	db.transaction{
	  db.execute("update pka set salt = '' where email = ?;", u_name)
	}
      rescue SQLite3::BusyException
	sleep(0.1)
	retry
      end
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
