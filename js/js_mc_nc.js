//Extract all data as MC or NC and returns

var col = [["content", "tag", "awordlength", "noofwords", "avgwordlength", "avgsentencelength", "linkdensity", 
            "fontSize", "fontWeight", "left", "top", "width", "height", "text", "atext"]];
var elementstofind = 'h, h1, h2, h3, h4, h5, h6, p, li, b, i, strong, em, div, font, span, code, time, label';
var totalwordnum = 0;

$("head").find('meta').each(function (index) {
  var row = [];
  if(this.getAttribute('name') == "title"){
    row.push("NC", this.tagName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    content = this.getAttribute('content').toString().replace(/,/g, "");
    name = this.getAttribute('name').toString().replace(/,/g, "");
    if(content != null && name != null)
      row.push(content, name);
    col.push(row);
  }
  if(this.getAttribute('name') == "author"){
    row.push("NC", this.tagName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    content = this.getAttribute('content').toString().replace(/,/g, "");
    name = this.getAttribute('name').toString().replace(/,/g, "");
    if(content != null && name != null)
      row.push(content, name);
    col.push(row);
  }
  if(this.getAttribute('property') == "og:url"){
    row.push("NC", this.tagName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    content = this.getAttribute('content').toString().replace(/,/g, "");
    property = this.getAttribute('property').toString().replace(/,/g, "");
    if(content != null && property != null)
      row.push(content, property);
    col.push(row);
  }
});

var row = []
row.push("NC", this.tagName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, window.location.hostname, "domain")
col.push(row);

$(document.getElementsByTagName("body")).find(elementstofind).each(function (index) {
  var text = "";
  for (var i = 0; i < this.childNodes.length; ++i){
    if (this.childNodes[i].nodeType === Node.TEXT_NODE || this.childNodes[i].nodeName == 'A')
      text += this.childNodes[i].textContent;
  }
  text = text.replace(/(\r\n|\n|\r)/gm, "").trim();
  var row = [];

  if(text.replace(/\s/g,"") != ""){

    var atext = "";
    $(this).find('a').each(function (index) {
      atext += this.textContent;
    });

    domRect = this.getBoundingClientRect();
    fontSize = parseFloat(window.getComputedStyle(this, null).getPropertyValue('font-size'));
    fontWeight = parseFloat(window.getComputedStyle(this, null).getPropertyValue('font-weight'));
    awordlength = strlen(atext);
    noofwords = strlen(text);
    avgwordlength = avgwordlen(text);
    avgsentencelength = noofwords / text.split(/\r\n|\r|\n/).length;
    linkdensity = awordlength/noofwords;
    totalwordnum += noofwords;

    var classx = this.className;
    if(classx.replace(/\s/g,"") != ""){
      if(this.className.search("_MAIN_CONTENT") != -1)
        row.push("MC");
      else
        row.push("NC");
    }
    else
      row.push("NC");

    row.push(this.tagName);
    row.push(awordlength);
    row.push(noofwords);
    row.push(avgwordlength);
    row.push(avgsentencelength);
    row.push(linkdensity);
    row.push(fontSize);
    row.push(fontWeight);
    row.push(this.getBoundingClientRect().left);
    row.push(this.getBoundingClientRect().top);
    row.push(this.getBoundingClientRect().width);
    row.push(this.getBoundingClientRect().height);
    row.push(text.toString().replace(/,/g, ""));
    row.push(atext.toString().replace(/,/g, ""));
    col.push(row);
  }
});

function avgwordlen(text){
  var totalwordchars = 0;
  words = text.split(' ');
  words.forEach(element => { totalwordchars += element.length; });
  return totalwordchars/words.length;
}

function strlen(text){
  str = text.replace(/(^\s*)|(\s*$)/gi,"");
  str = str.replace(/[ ]{2,}/gi," ");
  str = str.replace(/\n /,"\n");
  return str.split(' ').length;
}

row = [];
row.push("NC", this.tagName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, totalwordnum/arguments[0], "avgreadtime");
col.push(row);

return col;