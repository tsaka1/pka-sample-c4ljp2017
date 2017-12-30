// javascript example for public-key authentication

function gen_key(){
  var pass = document.forms[0].newpass.value;
  if (pass != document.forms[0].vrfy.value) {
    alert("Two passphrases are different.");
    return false;
  }
  document.forms[0].newpass.value = "";
  document.forms[0].vrfy.value = "";
  var keypair = KEYUTIL.generateKeypair("RSA", 2048);
  var prvkpem = KEYUTIL.getPEM(keypair.prvKeyObj, "PKCS5PRV", pass, "AES-256-CBC");
  localStorage["/~saka/pka4/ privateKey"] = prvkpem;
  var pubkpem = KEYUTIL.getPEM(keypair.pubKeyObj);
  localStorage["/~saka/pka4/ publicKey"] = pubkpem;
  document.forms[0].pubkey.value = pubkpem;
  return true;
}
