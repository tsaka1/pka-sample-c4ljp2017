// javascript example for public-key authentication

function send_sign(){
  prvkpem = localStorage["/~saka/pka4/ privateKey"];
  var pass = document.forms[0].pass.value;
  document.forms[0].pass.value = "";
  challenge = document.forms[0].challenge.value;
  var sig = new KJUR.crypto.Signature({"alg": "SHA256withRSA"});
  sig.init(prvkpem, pass);
  sig.updateString(challenge);
  var sigval = sig.sign();
  document.forms[0].sign.value = sigval;
  return true;
}
