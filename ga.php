<?php
// (c) z3n – R1V1@090617 – z3n666@gmail.com – www.overflow.biz
 
// Fake Resolutions
$resolutions=array("1024×768","1280×800","1280×1024","1440×900","1680×1050");
// Fake Flash Versions
$flash=array("10.0%20r2","10.0%20r1","9.0%20r12");
// Fake Languages
$languages=array("en-us","de","ja","ko","pt-br");
 
// functions
 
function baseurl($x) { //v1.03
 $y=str_replace("http://","",$x);
 $s=strpos($y,"/");
 if ($s === false) {
  $s=strpos($y,"?");
 }
 if ($s !== false) {
  $y=substr($y,0,$s);
 }
 return "http://".$y;
}
function getmicrotime() { list($usec, $sec) = explode(" ",microtime());return ((float)$usec + (float)$sec); }
function ga_fake($url,$ua) {
 global $resolutions,$flash,$languages;
 $gmt=round(getmicrotime(),0); // timestamp
 $uid=mt_rand(70710490,92710490); // unique id number
 $bid=mt_rand(21234567,91234567).mt_rand(1018864,9999999).mt_rand(1021,9999); // big random number
 $java=(rand(0,100) > 85) ? 0 : 1; // java enabled?
 $x="http://www.google-analytics.com/__utm.gif?utmwv=4.3&utmn=".mt_rand(64045995,94045995)."&utmhn=".str_replace("http://","",baseurl($url))."&utmcs=ISO-8859-1&utmsr=".$resolutions[array_rand($resolutions,1)]."&utmsc=32-bit&utmul=".$languages[array_rand($languages,1)]."&utmje=".$java."&utmfl=".$flash[array_rand($flash,1)]."&utmhid=".mt_rand(1650046796,1890046796)."&utmr=-&utmp=".str_replace(baseurl($url),"",$url)."&utmac=".$ua."&utmcc=__utma%3D".$uid.".".$bid.".".$gmt.".".$gmt.".".$gmt.".1%3B%2B__utmz%3D".$uid.".".$gmt.".1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none)%3B";
 @file_get_contents($x);
}
 
// now you just need to call it
 
ga_fake("http://javaongsan.github.com/","UA-35588905-1");
?>