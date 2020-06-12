// ==UserScript==
// @name         chaoxing-download
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  超星慕课资源下载提取
// @author       NL
// @match        https://*.chaoxing.com/mycourse/studentstudy?*
// @grant        none
// ==/UserScript==
function setDl(){
    var iframes = document.getElementById("iframe").contentWindow.document.querySelectorAll("iframe")
    for(let i=0;i<iframes.length;i++){
        if(iframes[i].getAttribute("objectId")==null){
            continue
        }
        var url = "http://d0.ananas.chaoxing.com/download/"+iframes[i].getAttribute("objectId")
        var a = document.createElement('a');
        a.setAttribute('href', url);
        a.setAttribute('class','downloadable-content')
        a.setAttribute('target','_blank')
        var textnode=document.createTextNode("↓下载课件")
        a.appendChild(textnode)
        if(iframes[i].parentElement.getElementsByClassName('downloadable-content').length==0){
    
            iframes[i].parentNode.insertBefore(a,iframes[i])
            console.log("inserted"+i)
        } else {//console.log('inserted already')
               //console.log(iframes[i].parentElement.getElementsByClassName('downloadable-content'))
        }
    }
    }
    (function() {
        'use strict';
        var old_text = "";
        console.log("downloader script running:");
        setTimeout(function (){
            old_text = document.getElementsByTagName("h1")[0].innerHTML;
            document.getElementsByTagName("h1")[0].innerHTML += "--->Waiting";
        },500);
        setTimeout(function(){
            var parent_node = document.getElementsByClassName("goback")[0]
            var bt = document.createElement("button")
            bt.innerHTML = "刷新下载"
            bt.onclick = function(){setDl()}
            parent_node.appendChild(bt)
        },500);
        setTimeout(function(){
            document.getElementsByTagName("h1")[0].innerHTML = old_text
            setDl()
        },1500);
        // Your code here...
    })();