#!/usr/local/bin/ruby
#
# An example of sign-in by public-key authentication
#

require("cgi")
require("cgi/session")
require("logger")
require("sqlite3")
require("securerandom")

load(Dir.getwd + "/config.rb")

log = Logger.new($log_file)
log.level = Logger::INFO

cgi = CGI.new
sess = CGI::Session.new(cgi, {
  "session_secure" => true,
  "tmpdir" => $sess_dir,
  "prefix" => $sess_prefix
  })

u_email = cgi["email"]

db = SQLite3::Database.new($db_name)
begin
  challenge = esc_tags(SecureRandom.hex(10) + Time.now.to_s)
  begin 
    db.transaction{
      db.execute("update pka set salt = ? where email = ?;", challenge, u_email)
    }
  rescue SQLite3::BusyException
    sleep(0.1)
    retry
  end
ensure
  db.close
end

cgi.out({
  "status" => "OK",
  "type" => "text/html",
  "charset" => "utf-8"
}) {
  <<-"EOS"
  <html>
  <head>
  <title>Public-key Authentication</title>
  <script type="text/javascript" src="jsrsasign-all-min.js"></script>
  </head>
  <body>
  <h1>Public-key Authentication</h1>
  <form method="POST" action="signin-pka2.cgi" onsubmit="return send_sign()">
    Passphrase: <input name="pass" type="password" size="20" /><br/>
    <input type="submit" />
    <input type="reset" />
    <input name="email" type="hidden" value="#{u_email}" /><br/>
    <input type="hidden" name="challenge" value="#{challenge}" />
    <input type="hidden" name="sign" value="" />
  </form>
  <hr/>
  <p>To register this service, please <a href="#{$sign_up_uri}">Sign-Up</a>.</p>
  <p>If you forgot your password, please follow
  <a href="#{$sign_up_uri}">Sign-Up</a> process to reset your password.</p>
  <script type="text/javascript" src="signin-pka1.js"></script>
  </body>
  </html>
  EOS
}

log.info($0) { "respond sign-in form." }

log.close
