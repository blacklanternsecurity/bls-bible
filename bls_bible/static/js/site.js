/*
# -------------------------------------------------------------------------------
# Copyright:   (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
*/
$(window).bind('popstate', function (event) {
  e = event.originalEvent;
  if (e.state){
    e.preventDefault();
    if (e.state.source == "local"){
      getContent(e.state.contentPath, true);
    }
    else if (e.state.source == "remote"){
      getContentRemote(e.state.contentPath, e.state.contentName, true);
    }
    else if (e.state.source == "" && e.state.contentPath == "" && e.state.contentName == ""){
      $('#file-content').modal('hide');
    }
  }
  return true;
});

$(window).on({
    'load': function() {
        window.history.pushState({
          contentPath: "",
          contentName: "",
          source: ""
        }, "");
        VerseOfTheDay();
    }
});

function toggleAptUiFilter(caller){
    $.ajax({
      url:"_filter_apts",
      data: {
        "apt": caller.value
      },
      type:'GET',
      success: function(dataStr){
        var data = dataStr.split('|');
        var flipper;
        // If we are checking/unchecking a box, then we want to increment/decrement our show/hide counter later
        if (caller.checked){
            flipper = 1;
        }
        else {
            flipper = -1;
        }

        // Grab the TTP section
        var ttpAccordion = document.getElementById("ttp-content");

        // Grab all of the child-containers in the TTP section
        var childContainers = ttpAccordion.getElementsByClassName("child-container");

        // If the containers textContent contains out filters, then flip the counter
        for (var i = 0; i < childContainers.length; i++){
            for (var j = 0; j < data.length; j++){
                if (childContainers[i].textContent.includes(data[j])){
                    childContainers[i].dataset.aptFilter = Number(childContainers[i].dataset.aptFilter) + flipper;
                }
            }
        }

        // Grab and alter the span counting active APT filters
        var aptHack = document.getElementById("APT-Filter-Active");
        aptHack.dataset.aptCounter = Number(aptHack.dataset.aptCounter) + flipper;

        if (Number(aptHack.dataset.aptCounter) == 0){
            // We have reset all the APT filters, show everything
            for (var i = 0; i < childContainers.length; i++){
                childContainers[i].style.display = "block";
            }
        }
        else{
            // We have at least one APT filter active, some hiding is necessary
            for (var i = 0; i < childContainers.length; i++){
                if (Number(childContainers[i].dataset.aptFilter) < 1){
                    childContainers[i].style.display = "none";
                }
                else{
                    childContainers[i].style.display = "block";
                }
            }
        }
      }
    });
}

function getContent(path, isBack=false){
  $.ajax({
    url:"_get_content",
    data: {
      "path": path
    },
    type:'GET',
    success: function(data){
      $('#advanced-search-modal').modal('hide');
      $('#file-content-body').html(data);
      $('#file-content').modal('show');
      $("#local-a").click(function(event){
        event.preventDefault();
      });
      if (!isBack){
        history.pushState({
          contentPath: path,
          source: "local"
        }, "");
      }
      
      clearSearch();
    }
  });
}

function getContentRemote(path, name, isBack=false){
  pathEnd = path.indexOf(name)
  shortPath = path.substring(0, pathEnd)
  $.ajax({
    url:"/_get_content_remote",
    data: {
      "path": shortPath,
      "name": name
    },
    type:'GET',
    success: function(data){
      $('#file-content-body').html(data);
      $('#file-content').modal('show');
      $("#local-a").click(function(event){
        event.preventDefault();
      });
      if (!isBack){
        history.pushState({
          contentPath: path,
          contentName: name,
          source: "remote"
        }, "");
      }

      clearSearch();
    }
  });
}

function searchLocal(tag){
  var osTags = [];
  $(".os-checkbox:checked").each(function(){
    osTags.push($(this).val());
  });

  var onpremTags = [];
  $(".onprem-checkbox:checked").each(function (){
    onpremTags.push($(this).val());
  });

  var cloudTags = [];
  $(".cloud-checkbox:checked").each(function (){
    cloudTags.push($(this).val());
  });

  var applicationTags = [];
  $(".application-checkbox:checked").each(function (){
    webTags.push($(this).val());
  });

  var specialTags = [];
  $(".special-checkbox:checked").each(function (){
    specialTags.push($(this).val());
  });

  var guideTtpTags = [];
  $(".guidettp-checkbox:checked").each(function (){
    guideTtpTags.push($(this).val());
  });

  var aptTags = [];
  $(".apt-checkbox:checked").each(function (){
    aptTags.push($(this).val());
  });

  $.ajax({
    url:"_search_local",
    data: {
      "tag": tag,
      "osTags": osTags,
      "onpremTags": onpremTags,
      "cloudTags": cloudTags,
      "applicationTags": applicationTags,
      "specialTags": specialTags,
      "guideTtpTags": guideTtpTags,
      "aptTags": aptTags
    },
    type:'GET',
    success: function(data){
      $('#searchResults').html(data);
      $('#searchResults')[0].style.display = 'block';
    }
  });
}

function clearSearch(){
  $('#searchResults').html("");
}

function VerseOfTheDay(){
    $.ajax({
      url: "_get_verse_of_the_day",
      type: 'GET',
      success: function(data){
        $('#VOTD-header').html("Verse of the Day" + "<br>" + data);
      }
    });
}


function showThing(thing,element) {
  $(".tooltiptext").text(thing);
  var rectLeft  = element.getBoundingClientRect().left+30;
  var rectTop = element.getBoundingClientRect().top - 40;
  $(".tooltiptext").css({top: rectTop, left: rectLeft});
  sleep(300);
  $(".tooltiptext").show();
}

function hideThing(){
  $(".tooltiptext").hide();
}

function clearFilters(){
var filters = $(".form-check-input")
for (i = 0; i < filters.length; i++){
  if (filters[i].classList.contains('apt-checkbox')){
    if (filters[i].checked){
      filters[i].checked = false;
      toggleAptUiFilter(filters[i]);
    }
  }
  else {
  	filters[i].checked = false;
  }
}}

function loadAPTs(){
  var ttps = document.getElementById("apt-filter-content").childElementCount;
  if (ttps == 0){
    $.ajax({
      url: "_get_apts",
      type:'GET',
      success: function(data){
        $('#apt-filter-content').html(data);
      }
    });
  }
  $('#filter-content-modal').modal('show');
}

function get_data_red(){
    $.ajax({
      url: "_get_data_red",
      type: 'GET',
      success: function(data){
        $('#red-content').html(data);
      }
    });
}

function get_data_blue(){
    $.ajax({
      url: "_get_data_blue",
      type: 'GET',
      success: function(data){
        $('#blue-content').html(data);
      }
    });
}

function get_data_ttp(){
    $.ajax({
      url: "_get_data_ttp",
      type: 'GET',
      success: function(data){
        $('#ttp-content').html(data);
      }
    });
}

function get_data_assessment(){
    $.ajax({
        url: "_get_data_assessment",
        type: 'GET',
        success: function(data){
            $('#assessment-content').html(data);
        }
    });
}

function get_data_purple(){
    $.ajax({
        url: "_get_data_purple",
        type: 'GET',
        success: function(data){
            $('#purple-content').html(data);
        }
    });
}

function get_data_apocrypha(){
    $.ajax({
        url: "_get_data_apocrypha",
        type: "GET",
        success: function(data){
            $('#apocrypha-content').html(data);
        }
    })
}

function doRecursiveHighlight(parts, ttpTitles, color, changeCount){
    // for ttp in ttpTitles
    for (var i = 0; i < ttpTitles.length; i++){
        // if ttp.innerText == parts[0]
        if (ttpTitles[i].innerText.includes(parts[0].replaceAll('_',' '))){
            if (color == "blue"){
                ttpTitles[i].dataset.blueToggleCount = Number(ttpTitles[i].dataset.blueToggleCount) + changeCount;
            }
            else if (color == "red"){
                ttpTitles[i].dataset.redToggleCount = Number(ttpTitles[i].dataset.redToggleCount) + changeCount;
            }
            else if (color == "ttp"){
                ttpTitles[i].dataset.ttpToggleCount = Number(ttpTitles[i].dataset.ttpToggleCount) + changeCount;
            }
            if (Number(ttpTitles[i].dataset.blueToggleCount) > 0 && Number(ttpTitles[i].dataset.redToggleCount) > 0){
                if (ttpTitles[i].childElementCount > 1){
                    ttpTitles[i].children[0].style.border = "2px solid purple";
                }
                else {
                    ttpTitles[i].style.border = "2px solid purple";
                }
            }
            else if (Number(ttpTitles[i].dataset.blueToggleCount) > 0){
                if (ttpTitles[i].childElementCount > 1){
                    ttpTitles[i].children[0].style.border = "2px solid blue";
                }
                else {
                    ttpTitles[i].style.border = "2px solid blue";
                }
            }
            else if (Number(ttpTitles[i].dataset.redToggleCount) > 0){
                if (ttpTitles[i].childElementCount > 1){
                    ttpTitles[i].children[0].style.border = "2px solid red";
                }
                else {
                    ttpTitles[i].style.border = "2px solid red";
                }
            }
            else if (Number(ttpTitles[i].dataset.ttpToggleCount) > 0){
                if (ttpTitles[i].childElementCount > 1){
                    ttpTitles[i].children[0].style.border = "2px solid rgb(255,127,0)";
                }
                else {
                    ttpTitles[i].style.border = "2px solid rgb(255,127,0)";
                }
            }
            else{
                if (ttpTitles[i].childElementCount > 1){
                    ttpTitles[i].children[0].style.border = "";
                }
                else{
                    ttpTitles[i].style.border = "";
                }

            }
            if (parts.length == 1){
                // We've matched our last part of the path
                return
            }
            var partsRemaining = parts.slice(1);
            var ttpTitlesRemaining = ttpTitles[i].parentElement.getElementsByClassName("accordion-header");
            doRecursiveHighlight(partsRemaining, ttpTitlesRemaining, color, changeCount);
        }
    }
}
function highlight_guides(event){
    var menu = $('#context-menu-ttp')[0].style.display = 'none';
    var path = event.data.param1;
    var caller = event.data.param2;
    var style = "";
    var changeCount = -1;
    $.ajax({
        url: "_highlight_guides",
        data: {
            "path": path
        },
        type: 'GET',
        success: function(data){
            var red_titles = [];
            var blue_titles = [];
            for (var i = 0; i < data['guides_referencing'].length; i++){
                if (data['guides_referencing'][i]['guide_color'] == "red"){
                    red_titles.push(data['guides_referencing'][i]['guide_path'])
                }
                if (data['guides_referencing'][i]['guide_color'] == "blue"){
                    blue_titles.push(data['guides_referencing'][i]['guide_path'])
                }
            }
            var blue_guides = document.getElementById("blue-content");
            var red_guides = document.getElementById("red-content");
            var blue_ui_titles = blue_guides.getElementsByClassName("accordion-header");
            var red_ui_titles = red_guides.getElementsByClassName("accordion-header");

            if (!caller.childNodes[1].classList.contains("toggledGuide")){
                caller.childNodes[1].classList.add("toggledGuide");
                changeCount = 1;
                caller.childNodes[1].dataset.toggleCount = Number(caller.childNodes[1].dataset.toggleCount) + changeCount;
                caller.childNodes[1].style.display = 'inline-flex'

                var recur = caller.parentNode.parentNode;
                while(recur){
                    if(recur.classList.contains("accordion-item")){
                        try{
                            recur.childNodes[0].childNodes[0].childNodes[1].classList.add("toggledGuide");
                            recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount = Number(recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount) + changeCount;
                            recur.childNodes[0].childNodes[0].childNodes[1].style.display = 'inline-flex';
                        }
                        catch (error) { break; }
                    }
                    recur = recur.parentNode;
                }
            }
            else{
                caller.childNodes[1].classList.remove("toggledGuide");
                caller.childNodes[1].dataset.toggleCount = Number(caller.childNodes[1].dataset.toggleCount) + changeCount;
                caller.childNodes[1].style.display = 'none';
                var recur = caller.parentNode.parentNode;
                while (recur){
                    if(recur.classList.contains("accordion-item")){
                        try{
                            recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount = Number(recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount) + changeCount;
                            if (Number(recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount) == 0){
                                recur.childNodes[0].childNodes[0].childNodes[1].classList.remove("toggledGuide");
                                recur.childNodes[0].childNodes[0].childNodes[1].style.display = 'none';
                            }
                        }
                        catch (error) { break; }
                    }
                    recur = recur.parentNode;
                }
            }
            if (data == "") { return; }
            var color = "ttp";
            for (var i = 0; i < red_titles.length; i++){
                var parts = red_titles[i].split('/');
                var parts = parts.slice(1);
                doRecursiveHighlight(parts, red_ui_titles, color, changeCount);
            }
            for (var i = 0; i < blue_titles.length; i++){
                var parts = blue_titles[i].split('/');
                var parts = parts.slice(1);
                doRecursiveHighlight(parts, blue_ui_titles, color, changeCount);

            }
        }
    });
}

function highlight_ttps(event){
    var menu = $('#context-menu-guide')[0].style.display = 'none';
    var path = event.data.param1;
    var color = event.data.param2;
    var caller = event.data.param3;
    var style = "";
    var changeCount = -1;
    $.ajax({
        url: "_highlight_ttps",
        data: {
            "path": path
        },
        type: 'GET',
        success: function(data){
            var titles = data.split('|');
            var ttps = document.getElementById("ttp-content");
            var ttpTitles = ttps.getElementsByClassName("accordion-header");
            if (!caller.childNodes[1].classList.contains("toggledTTP")){
                // node is not toggled, so we toggle, increment toggle count of TTPs and apply styles
                caller.childNodes[1].classList.add("toggledTTP");
                changeCount = 1;
                caller.childNodes[1].dataset.toggleCount = Number(caller.childNodes[1].dataset.toggleCount) + changeCount;
                caller.childNodes[1].style.display = 'inline-flex'
                // Toggle parents as well if they aren't already
                var recur = caller.parentNode.parentNode;
                while(recur){
                    if(recur.classList.contains("accordion-item")){
                        try {
                            recur.childNodes[0].childNodes[0].childNodes[1].classList.add("toggledTTP");
                            recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount = Number(recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount) + changeCount;
                            recur.childNodes[0].childNodes[0].childNodes[1].style.display = 'inline-flex';
                        }
                        catch (error) { break; }
                    }
                    recur = recur.parentNode;
                }
            }
            else{
                // Parent node is toggled, so we untoggle and remove styles
                caller.childNodes[1].classList.remove("toggledTTP");
                caller.childNodes[1].dataset.toggleCount = Number(caller.childNodes[1].dataset.toggleCount) + changeCount;
                caller.childNodes[1].style.display = 'none';
                var recur = caller.parentNode.parentNode;
                while(recur){
                    if(recur.classList.contains("accordion-item")){
                        try{
                            recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount = Number(recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount) + changeCount;
                            if (Number(recur.childNodes[0].childNodes[0].childNodes[1].dataset.toggleCount) == 0){
                                recur.childNodes[0].childNodes[0].childNodes[1].classList.remove("toggledTTP");
                                recur.childNodes[0].childNodes[0].childNodes[1].style.display = 'none';
                            }
                        }
                        catch (error) { break; }
                    }
                    recur = recur.parentNode;
                }
            }
            if (data == "") { return; }

            // Attempt recursive approach.
            for (var i = 0; i < titles.length; i++){
                var parts = titles[i].split('/');
                // Adjusting for base TTP folder
                var parts = parts.slice(1);
                doRecursiveHighlight(parts, ttpTitles, color, changeCount)
            }
        }
    });
}

function sleep(milliseconds){
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++){
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

function copyCode(number){
    id = 'codeblock-content-' + number;
    codeblock = document.getElementById(id);
    contents = codeblock.innerText;
    navigator.clipboard.writeText(contents.slice(0, -1));
}

function context(event, path, type, caller) {
    event.preventDefault();
    if (type == "red" || type == "blue"){
        var menu = document.querySelector('#context-menu-guide');
    }
    else if (type == "ttp" || type == "ttp-search"){
        var menu = document.querySelector('#context-menu-ttp');
    }
    menu.style.display = 'block';
    var x = event.clientX;
    var y = event.clientY;
    var xOffset = (window.pageXOffset || document.documentElement.scrollLeft) -
                    (document.documentElement.clientLeft || 0);
    var yOffset = (window.pageYOffset || document.documentElement.scrollTop) -
                    (document.documentElement.clientTop || 0);
    menu.style.left = x + xOffset + "px";
    menu.style.top = y + yOffset + "px";

    if (type == "red" || type == "blue"){
        var menuItem = $('#showTTPsContextItem');
        menuItem.off('click').click({
            param1: path,
            param2: type,
            param3: caller
        }, highlight_ttps);
    }
    else if (type == "ttp"){
        var menuItem = $('#addToProfileContextItem');
        menuItem.off('click').click({
            param1: path
        }, getProfilesForAdd);
        menuItem = $('#showGuidesContextItem');
        menuItem[0].style.display = 'list-item';
        menuItem.off('click').click({
            param1: path,
            param2: caller
        }, highlight_guides);
    }
    else if (type == "ttp-search"){
        var menuItem = $('#addToProfileContextItem');
        menuItem.off('click').click({
            param1: path
        }, getProfilesForAdd);
        menuItem = $('#showGuidesContextItem');
        menuItem.off('click');
        menuItem[0].style.display = 'none';
    }
}

function getProfilesForAdd(event){
    var path = event.data.param1;

    // We want to replace the context menu items with the currently available
    // profiles. Additionally, we want an option to add to a new profile

    // First we can hide the original context menu items
    var item1 = $('#addToProfileContextItem')[0];
    var item2 = $('#showGuidesContextItem')[0];

    item1.style.display = 'none';
    item2.style.display = 'none';

    // Second we can inject items for each profile we have
    // We need to get profiles from the app
    var dat = new Object();
    dat['path'] = path;

    $.ajax({
        url: "_get_groups_for_add_profile",
        data: {
            "data" : JSON.stringify(dat)
        },
        type: 'GET',
        success: function(data){
            var menu = $("#context-menu-ttp")[0].children[0];
            menu.innerHTML += data;
        }
    });
}

function addTTPToProfile(filePath, profileId){
    var dat = new Object();
    dat['filePath'] = filePath;
    dat['profileId'] = profileId;
    $.ajax({
        url: "_add_ttp_to_profile",
        data: {
            "data": JSON.stringify(dat)
        },
        type: 'GET',
        success: function(data){
            resetTTPContextMenu();
        }
    });
}

function resetTTPContextMenu(){
    var menu = $("#context-menu-ttp");
    menu[0].style.display = 'none';
    var adds = document.getElementsByClassName("add-to-profile-item");
    var len = adds.length
    for (var i = 0; i < len; i++){
        adds[0].remove();
    }
    var origs = menu[0].children[0].children;
    for (var i = 0; i < origs.length; i++){
        origs[i].style.display = 'list-item';
    }
}

function youClicked(event) {
    var menu = $("#context-menu-ttp");
    if (!menu.is(event.target) && menu.has(event.target).length === 0){
        resetTTPContextMenu();
    }
    var menu = $("#context-menu-guide");
    if (!menu.is(event.target) && menu.has(event.target).length === 0){
        menu[0].style.display = 'none';
    }
    var searchResults = $("#searchResults");
    if (!searchResults.is(event.target) && searchResults.has(event.target).length === 0){
        searchResults[0].style.display = 'none';
    }
}

function toggleContext(tog, menu){
    var active = 'context-menu--active';
    menu.dataset.menustate = tog;
    if (tog > 0){
        if (!menu.classList.contains(active)){
            menu.classList.add(active);
        }
    }
    else {
        if (menu.classList.contains(active)){
            menu.classList.remove(active);
        }
    }
}

function openInNewTab(path){
    $.ajax({
        url: "_get_tab_content",
            data: {
                "path": path
            },
            type: 'GET',
            success: function(data){
                var newTab = window.open('about:blank');
                newTab.document.open();
                newTab.document.write(data);
                newTab.document.close();
            }
        });
}

function editFile(path){
    $.ajax({
        url: "_edit_file",
        data: {
            "path": path
        },
        type: 'GET',
        success: function(data){
            var fileContainer = document.getElementsByClassName("modal-body")[0]
            fileContainer.innerHTML = data;
            createEditor("edit_textarea");
            editorSwap();
        }
    });
}

function saveFile(path){
    var newContent = document.getElementById("edit_textarea").value;
    $.ajax({
        url: "_save_file",
        data: {
            "path": path,
            "content": newContent
        },
        type: 'POST',
        success: function(){
            getContent(path);
            editorSwap();
        },
        fail: function(){
            alert('Failed to Save');
        }
    });
}

function cancelEditFile(path){
    getContent(path);
    editorSwap();
}

function editorSwap(){
    buttons = [
        "file-edit-btn",
        "file-save-btn",
        "file-undo-btn"
    ]

    buttons.forEach(function(id){
        btn = document.getElementById(id);
        if (btn.style.display == "none") {
            btn.style.display = "";
        }
        else {
            btn.style.display = "none";
        }
    });
}

function createEditor(id){
    var smde = new SimpleMDE({
        element: document.getElementById(id),
        autofocus: true,
        blockStyles: {
            bold: "**",
            italic: "_",
            code: "```"
        },
        forceSync: true,
        indentWithTabs: true,
        insertTexts: {
            horizontalRule: ["", "\n\n-----\n\n"]//,
            //image: ["![]/(http://",")"],
            //link: ["[", "](http://)"],
            //table: ["", "\n\n| Column 1 | Column 2 | Column 3 |\n| ------ | ------ | ------ |\n| Text | Text | Text |\n\n"]
        },
        lineWrapping: false,
        parsingConfig: {
            allowAtxHeaderWithoutSpace: true,
            strikethrough: false,
            underscoresBreakWords: true,
    	},
	    /*previewRender: function(plainText) {
		    return customMarkdownParser(plainText); // Returns HTML from a custom parser
	    },
	    previewRender: function(plainText, preview) { // Async method
		    setTimeout(function(){
			    preview.innerHTML = customMarkdownParser(plainText);
		    }, 250);_leader
            return "Loading...";
	    },*/
        promptURLs: true,
        renderingConfig: {
            singleLineBreaks: true,
            codeSyntaxHighlighting: true,
        },
        showIcons: ["code", "table"],
	    spellChecker: true,
	    status: ["autosave", "lines", "words", "cursor"],
	    styleSelectedText: true,
	    tabSize: 4,
	    toolbar: [
	        "bold",
	        "italic",
	        "strikethrough",
	        "|",
	        "heading-1",
	        "heading-2",
	        "heading-3",
	        "horizontal-rule",
	        "|",
	        "code",
	        "quote",
	        "|",
	        "unordered-list",
	        "ordered-list",
	        "|",
	        "link",
	        "image",
	        "table",
	        "|",
	        "preview",
	        "side-by-side",
	        "fullscreen"
        ],
	    toolbarTips: true,
    });
}

function showSettings(){
    $('#settings-modal').modal('show');
}

function showAdvancedSearch(){
    $('#advanced-search-modal').modal('show');
}

function submitAdvancedSearch(e, submitted){
    if (submitted === "key"){
        if (e.key !== "Enter"){
            return false;
        }
    }
    var regex = document.getElementById("regex-search-input").value;
    var context = document.getElementById("regex-context").value;
    $.ajax({
        url: "_search_advanced",
        data: {
            "regex": regex,
            "context": context
        },
        success: function(results){
            var resultsContainer = document.getElementById("advanced-search-results");
            resultsContainer.innerHTML = '';
            var row = document.createElement('div');
                row.classList = ['row advanced-search-row'];
                var col1 = document.createElement('div');
                col1.classList = ['col-sm-6 advanced-search-col'];
                var col2 = document.createElement('div');
                col2.classList = ['col-sm-6 advanced-search-col'];
                col1.innerHTML = '<b><center>File Matched</center></b>';
                col2.innerHTML = '<b><center>Strings Matched</center></b>';
                row.appendChild(col1);
                row.appendChild(col2);
                resultsContainer.appendChild(row);
            results['results'].forEach(function(result){
                var row = document.createElement('div');
                row.classList = ['row advanced-search-row'];
                var col1 = document.createElement('div');
                col1.classList = ['col-sm-6 advanced-search-col advanced-search-link'];
                var col2 = document.createElement('div');
                col2.classList = ['col-sm-6 advanced-search-col'];
                col1.innerHTML = result['path'].split('/Data/')[1];
                col1.setAttribute("onclick", "getContent('" + result['path'] + "')");
                var ul = document.createElement('ul');
                result['matches'].forEach(function(match){
                    var li = document.createElement('li');
                    var div = document.createElement('div');
                    div.innerHTML = match;
                    li.appendChild(div);
                    ul.appendChild(li);
                });
                col2.appendChild(ul);
                row.appendChild(col1);
                row.appendChild(col2);
                resultsContainer.appendChild(row);
            });
        }
    });
}

function get_theme(){
    $.ajax({
        url: "_get_theme",
        success: function(sheet){
            var head = document.head;
            var link = document.getElementById("theme-css-link");
            link.href = sheet;
            adjust_theme_select();
        }
    });
}

function adjust_theme_select(){
    var themeLink = document.getElementById("theme-css-link").href;
    var themeSelector = document.getElementById("theme-selector");
    for (var i = 0; i < themeSelector.length; i++){
        if (themeLink.includes(themeSelector[i].value)){
            themeSelector[i].selected = true;
            return true;
        }
    }
}

function change_theme(theme){
    var color = theme.value;
    $.ajax({
        url: "_change_theme",
        data: {
            "color": color
        },
        success: function(){
            $('#settings-modal').modal('hide');
            get_theme();
        }
    })
}

function updateData(){
    $('#row-content')[0].style.display = 'none';
    $('#update-select')[0].style.display = 'none';
    $('#loading-modal').modal({backdrop: 'static', keyboard: false});
    $('#loading-modal').modal('show');
    var content = document.getElementById("Data-Check").checked;
    var search = document.getElementById("Search-Index-Check").checked;
    var reverse = document.getElementById("Reverse-Reference-Check").checked;
    var apts = document.getElementById("APT-Check").checked;
    var attack = document.getElementById("ATT&CK-Check").checked;
    $.ajax({
      url:"_update",
      type:'GET',
      data: {
        "content": content,
        "search": search,
        "reverse": reverse,
        "apts": apts,
        "attack": attack
      },
      success: function(data){
        $('#leaderboard-header').html(data);
        $('#loading-modal').modal('hide');
        $('#row-content')[0].style.display = 'flex';
      }
    });
}

function showRanks(){
    $('#rank-modal').modal('show');
}

function populateTable(){
	$('#loading-modal').modal({backdrop: 'static', keyboard: false});
	$('#loading-modal').modal('show');
	$.ajax({
      url:"_get_leaderboard_content",
      type:'GET',
      success: function(data){
      	$('#leaderboard-table').html(data);
      	$('#loading-modal').modal('hide');
      }
    });
}

function sortTable(key) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("leaderboard-table");
  switching = true;
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = parseInt(rows[i].getElementsByTagName("TD")[key].innerHTML.replaceAll(',',''));
      y = parseInt(rows[i + 1].getElementsByTagName("TD")[key].innerHTML.replaceAll(',',''));
      if (x < y) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

// Threat Profiles

function loadGroups(){
    var modalBody  = document.querySelector('#groups-modal-content');
    $.ajax({
      url:"_get_groups",
        data: {},
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
            $('#groups-modal').modal('show');
        }
    });
}

function createGroup(){
    var modalBody = document.querySelector('#groups-modal-content');
    $.ajax({
        url:"_create_group",
        data: {},
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
        }
    });
}

function deleteGroup(id){
    var modalBody = document.querySelector('#groups-modal-content');
    $.ajax({
        url:"_delete_group",
        data: {
            "id": id
        },
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
        }
    });
}

function editGroup(id){
    $("#groups-modal").modal('hide');
    var modalBody = document.querySelector('#edit-group-modal-content');
    $.ajax({
      url:"_get_group_for_edit",
        data: {
            "id": id
        },
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
            $("#ttp-list").sortable();
            $("#edit-group-modal").modal('show');
        }
    })
}

function updateGroup(id){
    var modalBody = document.querySelector('#groups-modal-content');
    var name = $("#profile_name")[0].value;

    var ttps = [];
    var ttp_list = $("#ttp-list")[0];
    if (ttp_list) {
        for (var i = 0; i < ttp_list.childElementCount; i++){
            var filename = ttp_list.children[i].dataset.ttpFile;
            var ttpMajor = ttp_list.children[i].dataset.ttpMajor;
            var ttpMinor = ttp_list.children[i].dataset.ttpMinor;
            var ttp = {
                ttp_file: filename,
                ttp_major: ttpMajor,
                ttp_minor: ttpMinor
            };
            ttps.push(ttp);
        }
    }
    var dat = new Object();
    dat['id'] = id;
    dat['name'] = name;
    dat['ttps'] = ttps;
    $.ajax({
        url:"_update_group",
        data: {
            "data": JSON.stringify(dat)
        },
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
            $("#edit-group-modal").modal('hide');
            $("#groups-modal").modal('show');
        }
    });
}

function match_threat_profile(dat, selected_profiles){
    $.ajax({
        url: "_get_matching_profiles",
        data: {
            "data": JSON.stringify(dat)
        },
        type: 'GET',
        success: function(data){
            $("#groups-modal").modal('hide');
            var modalBody = document.querySelector('#match-profile-modal-body');
            modalBody.innerHTML = "";
            for (var i = 0; i < selected_profiles.length; i++){
                // Iterate over our selected profiles
                profile_header = "<div class='row profile-header-row'><div class='col-sm-12'>";
                profile_header += data[selected_profiles[i]]['name'] + " Matches:";
                profile_header += "</div></div>";
                modalBody.innerHTML += profile_header;
                for (var j = 0; j < data[selected_profiles[i]]['matches'].length; j++){
                    //Iterate over our matched results
                    profile_matches = "<div class='row profile-matches-row'>";
                    profile_matches += "<div class='col-sm-4'>";
                    profile_matches += data[selected_profiles[i]]['matches'][j][0] + ": ";
                    profile_matches += "</div>";
                    profile_matches += "<div class='col-sm-4'>";
                    profile_matches += data[selected_profiles[i]]['matches'][j][1] + "/" + data[selected_profiles[i]]['matches'][j][2];
                    profile_matches += "</div>";
                    profile_matches += "<div class='col-sm-4'>";
                    profile_matches += data[selected_profiles[i]]['matches'][j][3]
                    profile_matches += "</div>";

                    profile_matches += "</div>";
                    modalBody.innerHTML += profile_matches;
                }
            }
            $("#matched-profile-modal").modal('show');
        }
    });
}

function export_to_navigator(dat){
    $.ajax({
        url: "_export_to_navigator",
        data: {
            "data": JSON.stringify(dat)
        },
        type: 'GET',
        success: function(data){
            var a = document.createElement('a');
            var new_window = window.open();
            var fileurl = new_window.URL.createObjectURL(new Blob([data], {type: 'application/octet-stream'}));
            a.href = fileurl;
            a.download = 'navigator.json';
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            delete a;
            new_window.URL.revokeObjectURL(fileurl);
        }
    });
}

function open_profile_in_tabs(dat){
    $.ajax({
        url: "_open_profile_in_tabs",
        data: {
            "data": JSON.stringify(dat)
        },
        type: 'GET',
        success: function(data){
            files = data.split('|');
            for (var i = 0; i < files.length; i++){
                openInNewTab(files[i]);
            }
        }
    })
}

function export_profile_to_pdf(dat){
    $.ajax({
        url: '_export_profile_to_pdf',
        data: {
            "data": JSON.stringify(dat)
        },
        type: 'GET',
        success: function(path){
            window.open(path);
        }
    });
}

function threat_profile_action(){
    var action = $('#threat-profile-actions')[0].selectedOptions[0].value;
    var profiles = document.getElementsByClassName('threat-profile-check');
    var selected_profiles = [];
    for (var i = 0; i < profiles.length; i++){
        if (profiles[i].checked){
            selected_profiles.push(profiles[i].value);
        }
    }
    var dat = new Object();
    dat['profiles'] = selected_profiles;

    switch (action){
        case 'match':
            match_threat_profile(dat, selected_profiles)
            break;
        case 'navigator':
            export_to_navigator(dat);
            break;
        case 'tabs':
            open_profile_in_tabs(dat);
            break;
        case 'printable':
            export_profile_to_pdf(dat);
            break;
        default:
            break;
    }
    $('#groups-modal').modal('hide');
}

function removeTTP(ttp){
    ttp.parentElement.remove();
}

function showRightSide(){
    slideMainLeftOut();
    slideRightIn();
    var mainLeftBtn = document.getElementById("main-left-slide-btn");
    mainLeftBtn.style.display = "none";

    var mainRightBtn = document.getElementById("main-right-slide-btn");
    mainRightBtn.style.display = "none";

    var secondLeftBtn = document.getElementById("secondary-left-slide-btn");
    secondLeftBtn.style.display = "block";

}


// Variable Groups

function loadVariableGroups(){
    var modalBody  = document.querySelector('#variable-groups-modal-content');
    $.ajax({
      url:"_get_variable_groups",
        data: {},
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
            $('#variable-groups-modal').modal('show');
        }
    });
}

function createVariableGroup(){
    var modalBody = document.querySelector('#variable-groups-modal-content');
    $.ajax({
        url:"_create_variable_group",
        data: {},
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;

        }
    });
}

function createNewVariableGroup(){
    var type = document.getElementById("new_variable_group_select");
    var name = document.getElementById("new_variable_group_name").value;
    var selected = type.selectedOptions[0].value;
    $.ajax({
        url: "_create_new_variable_group",
        data: {
            "type": selected,
            "name": name
        },
        type: 'GET',
        success: function(data){
            var modalBody = document.querySelector('#variable-groups-modal-content');
            modalBody.innerHTML = data;
        }
    });
}

function deleteVariableGroup(id){
    var modalBody = document.querySelector('#variable-groups-modal-content');
    $.ajax({
        url:"_delete_variable_group",
        data: {
            "id": id
        },
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
        }
    });
}

function editVariableGroup(id, type){
    $("#variable-groups-modal").modal('hide');
    var modalBody = document.querySelector('#edit-variable-group-modal-content');
    $.ajax({
      url:"_get_variable_group_for_edit",
        data: {
            "id": id,
            "type": type
        },
        type:'GET',
        success: function(data){
            modalBody.innerHTML = data;
            $("#variable-list").sortable();
            $("#edit-variable-group-modal").modal('show');
        }
    })
}

function updateVariableGroup(id){

    var dat = new Object();
    dat['id'] = id;
    dat['type'] = document.getElementById("group_type").value;
    dat['name'] = document.getElementById("group_name").value;
    dat['domain_username'] = document.getElementById("group_domain_username").value;
    dat['email'] = document.getElementById("group_email").value;
    dat['domain_password'] = document.getElementById("group_domain_password").value;
    dat['domain_ntlm_hash'] = document.getElementById("group_domain_ntlm_hash").value;
    dat['kerberos_ticket'] = document.getElementById("group_kerberos_ticket").value;
    dat['notes'] = document.getElementById("group_notes").value;
    dat['where_local_admin'] = document.getElementById("group_where_local_admin").value;
    dat['privileges'] = document.getElementById("group_privileges").value;
    dat['potential_exploits'] = document.getElementById("group_potential_exploits").value;
    dat['confirmed_exploits'] = document.getElementById("group_confirmed_exploits").value;
    dat['vulnerabilities'] = document.getElementById("group_vulnerabilities").value;
    dat['local_only'] = document.getElementById("group_local_only").value;
    dat['local_access'] = document.getElementById("group_local_access").value;
    dat['certificate'] = document.getElementById("group_certificate").value;
    dat['has_sessions'] = document.getElementById("group_has_sessions").value;

    $.ajax({
        url:"_update_variable_group",
        data: {
            "data": JSON.stringify(dat)
        },
        type:'GET',
        success: function(data){
            $("#edit-variable-group-modal").modal('hide');
            loadVariableGroups();
        }
    });
}

function match_variable_group(dat, selected_profiles){
    $.ajax({
        url: "_get_matching_variable_groups",
        data: {
            "data": JSON.stringify(dat)
        },
        type: 'GET',
        success: function(data){
            $("#groups-modal").modal('hide');
            var modalBody = document.querySelector('#match-variable-group-modal-body');
            modalBody.innerHTML = "";
            for (var i = 0; i < selected_profiles.length; i++){
                // Iterate over our selected profiles
                profile_header = "<div class='row profile-header-row'><div class='col-sm-12'>";
                profile_header += data[selected_profiles[i]]['name'] + " Matches:";
                profile_header += "</div></div>";
                modalBody.innerHTML += profile_header;
                for (var j = 0; j < data[selected_profiles[i]]['matches'].length; j++){
                    //Iterate over our matched results
                    profile_matches = "<div class='row profile-matches-row'>";
                    profile_matches += "<div class='col-sm-4'>";
                    profile_matches += data[selected_profiles[i]]['matches'][j][0] + ": ";
                    profile_matches += "</div>";
                    profile_matches += "<div class='col-sm-4'>";
                    profile_matches += data[selected_profiles[i]]['matches'][j][1] + "/" + data[selected_profiles[i]]['matches'][j][2];
                    profile_matches += "</div>";
                    profile_matches += "<div class='col-sm-4'>";
                    profile_matches += data[selected_profiles[i]]['matches'][j][3]
                    profile_matches += "</div>";

                    profile_matches += "</div>";
                    modalBody.innerHTML += profile_matches;
                }
            }
            $("#matched-variable-group-modal").modal('show');
        }
    });
}

function variable_group_action(){
    var action = $('#variable-group-actions')[0].selectedOptions[0].value;
    var profiles = document.getElementsByClassName('variable-group-check');
    var selected_variable_groups = [];
    for (var i = 0; i < profiles.length; i++){
        if (vargroups[i].checked){
            selected_vargroups.push(vargroups[i].value);
        }
    }
    var dat = new Object();
    dat['vargroups'] = selected_vargroups;

    switch (action){
        case 'Return Compromised Targets':
            get_compromised(dat, selected_vargroups)
            break;
        case 'Summarize Domain Variables':
            summarizeDomainVariables(dat);
            break;
        default:
            break;
    }
    $('#groups-modal').modal('hide');
}



// More functions



function closeRightSide(){
    slideRightOut();
    slideMainRightIn();
    var mainLeftBtn = document.getElementById("main-left-slide-btn");
    mainLeftBtn.style.display = "block";

    var mainRightBtn = document.getElementById("main-right-slide-btn");
    mainRightBtn.style.display = "block";

    var secondLeftBtn = document.getElementById("secondary-left-slide-btn");
    secondLeftBtn.style.display = "none";
}

function showLeftSide(){
    slideMainRightOut();
    slideLeftIn();
    var mainLeftBtn = document.getElementById("main-left-slide-btn");
    mainLeftBtn.style.display = "none";

    var mainRightBtn = document.getElementById("main-right-slide-btn");
    mainRightBtn.style.display = "none";

    var secondRightBtn = document.getElementById("secondary-right-slide-btn");
    secondRightBtn.style.display = "block";
}

function closeLeftSide(){
    slideLeftOut();
    slideMainLeftIn();
    var mainLeftBtn = document.getElementById("main-left-slide-btn");
    mainLeftBtn.style.display = "block";

    var mainRightBtn = document.getElementById("main-right-slide-btn");
    mainRightBtn.style.display = "block";

    var secondRightBtn = document.getElementById("secondary-right-slide-btn");
    secondRightBtn.style.display = "none";
}

function slideMainLeftOut(){
    var $main = document.getElementById("main-accordion-content");
    $main.classList.add("slide-out-left");
    $main.classList.remove("slide-in-right")
    $main.classList.remove("slide-in-left");
}

function slideMainRightOut(){
    var $main = document.getElementById("main-accordion-content");
    $main.classList.remove("slide-in-right");
    $main.classList.remove("slide-in-left");
    $main.classList.add("slide-out-right");
}

function slideMainRightIn(){
    var $main = document.getElementById("main-accordion-content");
    $main.classList.add("slide-in-left");
    $main.classList.remove("slide-out-left");
}

function slideMainLeftIn(){
    var $main = document.getElementById("main-accordion-content");
    $main.classList.add("slide-in-right");
    $main.classList.remove("slide-out-right");
}

function slideRightIn(){
    var $right = document.getElementById("right-accordion-content");
    $right.classList.add("slide-in-right");
    $right.classList.remove("slide-out-right");
}

function slideRightOut(){
    var $right = document.getElementById("right-accordion-content");
    $right.classList.add("slide-out-right");
    $right.classList.remove("slide-in-right");
}

function slideLeftIn(){
    var $left = document.getElementById("left-accordion-content");
    $left.classList.add("slide-in-left");
    $left.classList.remove("slide-out-left");
}

function slideLeftOut(){
    var $left = document.getElementById("left-accordion-content");
    $left.classList.add("slide-out-left");
    $left.classList.remove("slide-in-left");
}


