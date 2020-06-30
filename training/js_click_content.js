//Rip data from text blocks into CSV depending on where user clicks

var col = [["content", "tag", "awordlength", "noofwords", "avgwordlength", "avgsentencelength", "linkdensity", 
            "fontSize", "fontWeight", "left", "top", "width", "height", "text", "atext"]];

window.onmousedown=function(e) {
  $('a').click(function () {
    return false;
  });
  e.target.className += "_MAIN_CONTENT";
  e.target.style.backgroundColor = "red";
};

function extract() {

  var elementstofind = 'h, h1, h2, h3, h4, h5, h6, p, li, b, i, strong, em, div, font, span, code, time, label';
  $(document.getElementsByTagName("body")).find(elementstofind).each(function (index) {
    var text = "";
    console.log(`this element = ${this.tagName} / ${this.className}`);
    for (var i = 0; i < this.childNodes.length; ++i){
      console.log(`a nodeType = ${this.childNodes[i].nodeType} / nodeName = ${this.childNodes[i].nodeName}`);
      if (this.childNodes[i].nodeType === Node.TEXT_NODE || this.childNodes[i].nodeName == 'A'){
        text += this.childNodes[i].textContent;
        console.log(`inside i = ${i} / this.childNodes[i].textContent - ${this.childNodes[i].textContent} / text : ${text}`);
      }
    }
    text = text.replace(/(\r\n|\n|\r)/gm, "").trim();
    var row = [];

    //If text is not empty or filled with whitespaces
    if(text.replace(/\s/g,"") != ""){

      var atext = "";
      $(this).find('a').each(function (index) {
        console.log(`this.textContent - ${this.textContent}`);
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

      var classx = this.className;
      console.log("CHECK - ",classx ," | ",classx.search("_MAIN_CONTENT"));
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
      row.push(text.toString().toLowerCase().replace(/,/g, ""));
      row.push(atext.toString().toLowerCase().replace(/,/g, ""));
      col.push(row);
      console.log(`row = ${row}`);
    }
  });
}

$('a').on('onclick',function(e) {
  console.log(`pls dont jump`);
});

$(document).on('keydown',function(e) {
  if(e.which == 18) { //Alt
    extract();
    console.log(`col = ${col}`);
    var filename = window.location.href;
    var element = document.createElement("a");
    var lop = col.map(e => e.join(",")).join("\n");
    var idk = 'data:text/csv;charset=utf-8-sig,' + encodeURIComponent(lop);
    element.setAttribute("href", idk);
    element.setAttribute("download", `${filename}.csv`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
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