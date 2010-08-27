// Preload images function (http://www.mattfarina.com/2007/02/01/preloading_images_with_jquery)
$.preloadImages = function() {for(var i = 0; i<arguments.length; i++) {jQuery("<img>").attr("src", arguments[i]);}}
var last_lexer = '';
var current_copy;

// When the page is ready (jQuery shortcut).
$(function() {
    
    var clip = null;
	clip = new ZeroClipboard.Client();
	clip.setHandCursor( true );
	clip.setText(' ');
	$('a.copy').live('mouseover', function() {
		clip.setText( $(this).parent().parent().parent().children('.code').html().replace(/\&gt;/g, '>').replace(/\&lt;/g, '<') );
		current_copy = $(this).parent().parent().parent().children('div').children('.highlight');
		if (clip.div) {
			clip.receiveEvent('mouseout', null);
			clip.reposition(this);
		}
		else clip.glue(this);
		clip.receiveEvent('mouseover', null);
	});
    
    // Blink Mr. Tweet.
    Blink();
    
    // Bind Mr. Tweet.
    $('#mr-tweet').mouseover(function(){BlinkOnce()});
    
    // Autogrow add code.
    $('#code-0').autogrow();
    
    // Autogrow comment.
    $('#id_comment').autogrow();
    
    $('.mini-search').focus(function() {
        if ($(this).attr('value') == 'search snipt') {
            $(this).data('orig', $(this).attr('value'));
            $(this).attr('value', '');
        }
    });
    $('.mini-search').blur(function() {
        if ($(this).attr('value') == '') {
            $(this).attr('value', $(this).data('orig'));
        }
    });
    
    // Bind add snipt toggle to buttons.
    $('.add-snipt').bind('click', function() {$('#userpage-add-snipt').slideToggle(); return false;})
    
    if (window.location.hash != '') {
        // Open the add snipt dialogue if we have a hash '#add'.
        if (window.location.hash == '#add') {
            $('#userpage-add-snipt').slideToggle();
        } else {
            $(window.location.hash + ' .body').effect("highlight", {color: '#527A9E'}, 750);
        }
    }
    
    if (typeof(mine) != 'undefined') {
        if (mine) {
            $('.add-snipt-header').bind('click', function() {$('#userpage-add-snipt').slideToggle(); return false;})
        }
    }
    
    // Any anchor swith class toggle-add should trigger the add snipt form.
    $('.toggle-add').bind('click', function() {$('#userpage-add-snipt').slideToggle();});
    
    $('#lexer-0').keypress(function(e) {if(e.keyCode == 13) {Save(0); return false;}});
    
    $('#wrap-check').bind('click', function() {
        $('#loading-wrap, #wrap-text').toggle();
        $.ajax({
            type: 'GET',
            url: '/wrap/toggle',
            success: function() {
                $('#loading-wrap, #wrap-text').toggle();
                if ($('.highlight pre').css('white-space') == 'pre') {
                    $('.highlight pre').css('white-space', 'pre-wrap');
                    $('head').append('<style type="text/css">.highlight pre {white-space: pre-wrap;}</style>');
                }
                else {
                    $('.highlight pre').css('white-space', 'pre');
                    $('head').append('<style type="text/css">.highlight pre {white-space: pre;}</style>');
                }
            }
        });
    });
    
    // If user already has a snipt, use the last lexer for the selected value.
    if (last_lexer != '') {
        $('#lexer-0 option').filter(':selected').attr('selected', false);
        $("#lexer-0 option[value='" + last_lexer + "']").attr('selected', true);
    }
    
    /**
     * Live query is better than sliced bread.  It makes our bindings persistent.  See http://brandonaaron.net/docs/livequery/.
     * Anywho, bind the edit function to each snipt's edit link.
     */
    $('.edit').livequery('click', function() {
        
        // This is quite ugly, but it references the list item of the snipt so we can access its contents later.
        var container = $(this).parent().parent().parent();
        
        // Grab the height of the current code block, so we can use that for the textarea height.
        var height = container.children('.code').height() + 'px';
        
        var id = container.children('.code').attr('id');
        
        /**
         * If the snipt already contains a textarea element within it, then the user has either clicked 'cancel',
         * or the form has been submitted, where we would programatically trigger this function.
         */
        if (container.children('textarea').length > 0) {
            
            /**
             * This whole section should be reorganized.
             * Idealy, we simply store links and elements in a more contained manner, rather than treating each element differently.
             */

            $('#public-flag-' + id.replace('code-','')).css('visibility','visible');
            
            // Hide the code textarea.
            container.children('.code').css('display', 'none');
            
            // Show the highlighted code block.
            container.children('div').children('.highlight').css('display', 'block');
            
            // Remove the active class on the containing list item.
            container.removeClass('active');
            
            // Remove the save link.
            $(this).parent().children('.save').remove();
            
            // Remove the active class from the edit link.
            $(this).html('edit').removeClass('active');
            
            // Replace the code textarea with the original code block.
            container.children('textarea').replaceWith($(this).data('orig'));
            
            // Replace the description textarea with the original description block.
            container.children('.description').replaceWith($(this).data('orig-desc'));
            
            // Replace the delete link with the copy link.
            $(this).parent().children('.delete').replaceWith($(this).data('copy'));
            
            $('.embed-' + id.replace('code-','')).css('display', 'block');
            
            // Hide the tags input field.
            container.children('p').children('.tags').css('display', 'none');
            
            // Remove the lexers list.
            container.children('.tools').children('.tools-container').children('select').remove();
            
            // Remove the public option.
            container.children('.tools').children('.tools-container').children('.make-public').remove();
            
            // Show the tags list.
            container.children('.snipt-tags').css('display', 'block');
            container.children('.posted-by').css('display', 'block');
            
            // Show the top and bottom pieces to the code block (nice rounded corners).
            container.children('.top, .bottom').css('display', 'block');
        }
        
        /**
         * If the snipt does not already contain a textarea element within it, then the user has clicked 'edit',
         * and we must construct the appropriate textareas for it.
         */
        else {
            
            // Harvest the id of this snipt.
            id = id.replace('code-', '');
            
            $('#public-flag-' + id).css('visibility','hidden');
            
            // Change the edit link to a cancel link, though its onclick will still trigger the same function (the livequery edit function).
            $(this).attr('id', 'cancel-' + id).html('cancel').addClass('active');
            
            // Set list item to active.
            container.addClass('active');
            
            // Create save and delete links to be used later.
            var save = '<span class="right separator save">|</span><a href="#" class="save right active" id="save-' + id + '" onclick="Save(' + id + '); return false;">save</a>';
            var del = '<a href="#" class="delete right active" id="delete-' + id + '" onclick="Delete(' + id + ', this); return false;">delete</a>';
            
            /**
             * Append the save link to directly after this element (next to the edit link).
             * Note that the elements are floated right, which is why we add in this order.
             */
            $(this).after(save);
            
            // Hide the highlighted code block.
            container.children('div').children('.highlight').css('display', 'none');
            
            /**
             * Save the original copy link on this element for access after editing is over.
             * See more here: http://docs.jquery.com/Internals/jQuery.data
             */
            $(this).data('orig', container.children('.code'));
            $(this).data('copy', $('#copy-' + id));
            
            // Replace the copy link with a delete link.
            $('#copy-' + id).replaceWith(del);
            
            $('.embed-' + id).css('display', 'none');
            
            // Replace the original code block with the edit textarea.
            container.children('.code').replaceWith('<textarea name="code" class="code" id="code-' + id + '" style="height: ' + height + '; min-height: ' + height + ';" rows="10" cols="10">' + container.children('.code').html() + '</textarea>');
            
            // Save the original description for use later, and replace it with a textarea.
            $(this).data('orig-desc', $('#description-' + id));
            $('#description-' + id).replaceWith('<input name="description" class="description" id="description-' + id + '" value="' + $('#description-raw-' + id).html() + '" />');
            
            // Prepend the lexers list.
            container.children('.tools').children('.tools-container').prepend(BuildLexers(id));
            
            // Prepend the public option.
            if ($('#public-raw-' + id).html() == '1' || $('#public-raw-' + id).html() == 'true') {
                var checked = ' checked="checked"';
            } else {
                var checked = '';
            }
            container.children('.tools').children('.tools-container').prepend('<div class="make-public right"><input type="checkbox" name="public" id="public-' + id + '"' + checked + ' /> <label for="public-' + id + '">public</label></div>');
            
            // Hide the tags list, and show the tags input field.
            container.children('.snipt-tags').css('display', 'none');
            container.children('.posted-by').css('display', 'none');
            $('#tags-' + id).css('display', 'block');
            
            // Hide the top and bottom to the code block (rounded corners).
            container.children('.top, .bottom').css('display', 'none');
            
            // Set the textareas autogrow.
            container.children('textarea').autogrow().focus();
            
            // Bind lexer input to submit.
            
            $('#lexer-' + id).keypress(function(e) {if(e.keyCode == 13) {Save(id); return false;}});
        }
        return false;
    });
});

function BlinkOnce() {
    $("#blink").show();
    setTimeout("$('#blink').hide();", 100);
    return false;
}

function Blink() {
    $("#blink").show();
    setTimeout("$('#blink').hide();", 100);
    BlinkCallback();
    return false;
}
function BlinkCallback() {
    setTimeout("Blink();", Math.floor(Math.random() * (7000 - 3000)) + 3000);
}

function DisableMessage() {
    $.get('/message/toggle');
    $('.message').toggle();
    return false;
}

function BuildLexers(id) {
    var lexers = [{'id': 'as', 'name': 'ActionScript'},{'id': 'as3', 'name': 'ActionScript 3'},{'id': 'apacheconf', 'name': 'ApacheConf'},{'id': 'applescript', 'name': 'AppleScript'},{'id': 'bbcode', 'name': 'BBCode'},{'id': 'bash', 'name': 'Bash'},{'id': 'bat', 'name': 'Batchfile'},{'id': 'befunge', 'name': 'Befunge'},{'id': 'boo', 'name': 'Boo'},{'id': 'brainfuck', 'name': 'Brainfuck'},{'id': 'c', 'name': 'C'},{'id': 'csharp', 'name': 'C#'},{'id': 'cpp', 'name': 'C++'},{'id': 'css', 'name': 'CSS'},{'id': 'css+django', 'name': 'CSS+Django/Jinja'},{'id': 'css+genshitext', 'name': 'CSS+Genshi Text'},{'id': 'css+mako', 'name': 'CSS+Mako'},{'id': 'css+myghty', 'name': 'CSS+Myghty'},{'id': 'css+php', 'name': 'CSS+PHP'},{'id': 'css+erb', 'name': 'CSS+Ruby'},{'id': 'css+smarty', 'name': 'CSS+Smarty'},{'id': 'cheetah', 'name': 'Cheetah'},{'id': 'clojure', 'name': 'Clojure'},{'id': 'common-lisp', 'name': 'Common Lisp'},{'id': 'd', 'name': 'D'},{'id': 'dpatch', 'name': 'Darcs Patch'},{'id': 'control', 'name': 'Debian Control file'},{'id': 'sourceslist', 'name': 'Debian Sourcelist'},{'id': 'delphi', 'name': 'Delphi'},{'id': 'diff', 'name': 'Diff'},{'id': 'django', 'name': 'Django/Jinja'},{'id': 'dylan', 'name': 'Dylan'},{'id': 'erb', 'name': 'ERB'},{'id': 'erlang', 'name': 'Erlang'},{'id': 'fortran', 'name': 'Fortran'},{'id': 'gas', 'name': 'GAS'},{'id': 'genshi', 'name': 'Genshi'},{'id': 'genshitext', 'name': 'Genshi Text'},{'id': 'pot', 'name': 'Gettext Catalog'},{'id': 'gnuplot', 'name': 'Gnuplot'},{'id': 'groff', 'name': 'Groff'},{'id': 'html', 'name': 'HTML'},{'id': 'html+cheetah', 'name': 'HTML+Cheetah'},{'id': 'html+django', 'name': 'HTML+Django/Jinja'},{'id': 'html+genshi', 'name': 'HTML+Genshi'},{'id': 'html+mako', 'name': 'HTML+Mako'},{'id': 'html+myghty', 'name': 'HTML+Myghty'},{'id': 'html+php', 'name': 'HTML+PHP'},{'id': 'html+smarty', 'name': 'HTML+Smarty'},{'id': 'haskell', 'name': 'Haskell'},{'id': 'ini', 'name': 'INI'},{'id': 'irc', 'name': 'IRC logs'},{'id': 'io', 'name': 'Io'},{'id': 'java', 'name': 'Java'},{'id': 'jsp', 'name': 'Java Server Page'},{'id': 'js', 'name': 'JavaScript'},{'id': 'js+cheetah', 'name': 'JavaScript+Cheetah'},{'id': 'js+django', 'name': 'JavaScript+Django/Jinja'},{'id': 'js+genshitext', 'name': 'JavaScript+Genshi Text'},{'id': 'js+mako', 'name': 'JavaScript+Mako'},{'id': 'js+myghty', 'name': 'JavaScript+Myghty'},{'id': 'js+php', 'name': 'JavaScript+PHP'},{'id': 'js+erb', 'name': 'JavaScript+Ruby'},{'id': 'js+smarty', 'name': 'JavaScript+Smarty'},{'id': 'llvm', 'name': 'LLVM'},{'id': 'lighty', 'name': 'Lighttpd config'},{'id': 'lhs', 'name': 'Literate Haskell'},{'id': 'logtalk', 'name': 'Logtalk'},{'id': 'lua', 'name': 'Lua'},{'id': 'moocode', 'name': 'MOOCode'},{'id': 'basemake', 'name': 'Makefile'},{'id': 'make', 'name': 'Makefile'},{'id': 'mako', 'name': 'Mako'},{'id': 'matlab', 'name': 'Matlab'},{'id': 'matlabsession', 'name': 'Matlab session'},{'id': 'minid', 'name': 'MiniD'},{'id': 'trac-wiki', 'name': 'MoinMoin/Trac Wiki'},{'id': 'mupad', 'name': 'MuPAD'},{'id': 'mysql', 'name': 'MySQL'},{'id': 'myghty', 'name': 'Myghty'},{'id': 'nasm', 'name': 'NASM'},{'id': 'nginx', 'name': 'Nginx configuration file'},{'id': 'numpy', 'name': 'NumPy'},{'id': 'ocaml', 'name': 'OCaml'},{'id': 'objective-c', 'name': 'Objective-C'},{'id': 'php', 'name': 'PHP'},{'id': 'pov', 'name': 'POVRay'},{'id': 'perl', 'name': 'Perl'},{'id': 'python', 'name': 'Python'},{'id': 'python3', 'name': 'Python 3'},{'id': 'py3tb', 'name': 'Python 3.0 Traceback'},{'id': 'pytb', 'name': 'Python Traceback'},{'id': 'pycon', 'name': 'Python console session'},{'id': 'rhtml', 'name': 'RHTML'},{'id': 'raw', 'name': 'Raw token data'},{'id': 'redcode', 'name': 'Redcode'},{'id': 'rb', 'name': 'Ruby'},{'id': 'rbcon', 'name': 'Ruby irb session'},{'id': 'splus', 'name': 'S'},{'id': 'sql', 'name': 'SQL'},{'id': 'scala', 'name': 'Scala'},{'id': 'scheme', 'name': 'Scheme'},{'id': 'smalltalk', 'name': 'Smalltalk'},{'id': 'smarty', 'name': 'Smarty'},{'id': 'squidconf', 'name': 'SquidConf'},{'id': 'tcl', 'name': 'Tcl'},{'id': 'tcsh', 'name': 'Tcsh'},{'id': 'tex', 'name': 'TeX'},{'id': 'text', 'name': 'Text only'},{'id': 'vb.net', 'name': 'VB.net'},{'id': 'vim', 'name': 'VimL'},{'id': 'xml', 'name': 'XML'},{'id': 'xml+cheetah', 'name': 'XML+Cheetah'},{'id': 'xml+django', 'name': 'XML+Django/Jinja'},{'id': 'xml+mako', 'name': 'XML+Mako'},{'id': 'xml+myghty', 'name': 'XML+Myghty'},{'id': 'xml+php', 'name': 'XML+PHP'},{'id': 'xml+erb', 'name': 'XML+Ruby'},{'id': 'xml+smarty', 'name': 'XML+Smarty'},{'id': 'xslt', 'name': 'XSLT'},{'id': 'yaml', 'name': 'YAML'},{'id': 'c-objdump', 'name': 'c-objdump'},{'id': 'cpp-objdump', 'name': 'cpp-objdump'},{'id': 'd-objdump', 'name': 'd-objdump'},{'id': 'objdump', 'name': 'objdump'},{'id': 'rst', 'name': 'reStructuredText'},{'id': 'sqlite3', 'name': 'sqlite3con'}];
    
    var content ='<select name="lexer" class="edit-lexers" id="lexer-' + id + '">';
    var selected = '';
    for (var i = 0; i < lexers.length; i++) {
        if ($('#lexer-raw-' + id).html() == lexers[i].id) {
            selected = ' selected="selected"';
        }
        else {
            selected = '';
        }
        content += '<option' + selected + ' value="' + lexers[i].id + '">' + lexers[i].name + '</option>';
    }
    content += '</select>';
    
    return content;
}

function Delete(id, obj) {
    /**
     * Handle the deletion of a snipt.
     * Ask for confirmation via confirm(), then make the request to the server to delete.
     */
    if (confirm('Are sure you want to delete that?')) {
        $(obj).parent().html('<span class="delete right active" style="color: red; display: block; padding: 10px 10px 5px;">deleting...</span>');
        $.ajax({
            type: 'post',
            url: '/delete/',
            dataType: 'json',
            data: {
                'id': id
            },
            success: function(resp) {
                
                // The server responds with the id of the snipt that was deleted, so we make it disappear.
                $('.container-' + resp.id).slideToggle();
                
                // Rebuild the user tags list.
                $.getJSON('/tags/list', function(json) {RebuildUserTags(json)});
            }
        });
    }
    return false;
}

function RebuildSniptTags(tags, obj) {
    /**
     * Rebuild the tag list when a snipt is edited.
     */
    
    var content = '';
    for (var i = 0; i < tags.length; i++) {
        if ((i + 1) != tags.length) {
            var sep = ',&nbsp;';
        } else {
            var sep = '';
        }
        content += '<li><a href="/' + username + '/tag/' + tags[i].tag + '">' + tags[i].tag + '</a>' + sep + '</li>';
    }
    
    // Replace the snipt's current tag list with the new tag list.
    obj.html(content);
}

function RebuildUserTags(tags) {
    /**
     * Rebuild the user tag list.
     */
    
    var content = '';
    tags = tags.tags_list;
    for (var i = 0; i < tags.length; i++) {
        if (request_tag == tags[i].tag) {
            var active = ' class="active"';
        } else {
            var active = '';
        }
        content += '<li><a href="/' + username + '/tag/' + tags[i].tag + '"' + active + '>' + tags[i].tag + ' (' + tags[i].count + ')</a></li>';
    }
    $('#user-tags').html(content);
}

function Save(id) {
    /**
     * Handle both the creation of a new snipt, and the modification of an existing snipt.
     */
    
    // If we sent along an id that was undefined, then we're adding a new snipt.
    if (typeof(id) == 'undefined') {
        
        // We set the id to 0, because that's what the ids on the add form use.
        id = 0;
    }
    
    var description = $('#description-' + id).attr('value');
    var tags = $('#tags-' + id).attr('value');
    var lexer = $('#lexer-' + id + ' option').filter(':selected').attr('value');
    
    if ($('#public-' + id).attr('checked') == true) {
        var pub = 'True';
    } else {
        var pub = 'False';
    }
    
    if (tags == '') {
        alert('Please enter at least one tag.');
        $('#tags-0').focus();
        return false;
    }
    
    // Check to make sure we've entered data for code, description, and tags. Otherwise, return false.
    if ($('#code-' + id).attr('value') != '' && description != '') {
        
        // If this is a new snipt, replace the submit links with a message.
        if (id == 0) {
            $('.submit').html('<span style="color: green">adding...</span>');
        }
        
        /**
         * Otherwise, if we're modifying an existing snipt, replace the save link with a message.
         * There could probably be more consistency here combining the above submit message.
         */
        else {
            $('#save-' + id).replaceWith('<span class="save right active" style="color: green; display: block; padding: 10px 10px 5px;">saving...</span>');
        }
        
        // Make the post request to the server.
        $.ajax({
            type: 'post',
            url: '/save/',
            dataType: 'json',
            data: {
                'id': id,
                'code': $('#code-' + id).attr('value'),
                'description': description,
                'tags': tags,
                'lexer': lexer,
                'public': pub,
            },
            success: function(resp) {
                
                // Click the cancel link, triggering the removal of the textareas, among other things.
                $('#cancel-' + id).click();
                
                // Change the HTML of the original code, description and tags blocks to the new code as returned by the server.
                $('#code-' + id).html(resp.code);
                var publicSaved = $('#public-flag-' + id).clone();
                $('#code-stylized-' + id).html(resp.code_stylized).prepend(publicSaved);
                $('#description-raw-' + id).html(resp.description);
                $('#tags-' + id).html(resp.tags);
                $('#lexer-raw-' + id).html(resp.lexer);
                $('#public-raw-' + id).html('' + resp.public);
                
                if (resp.public) {
                    $('#public-flag-' + id).css('display', 'block');
                    var key = '';
                } else {
                    $('#public-flag-' + id).css('display', 'none');
                    var key = '?key=' + resp.key;
                }
                
                $('#description-' + id).html('<a title="Permalink for this snipt" href="/' + resp.username + '/' + resp.slug + key + '"><span class="permaslug">&#8734;</span> ' + resp.description + '</a>');
                
                // Rebuild the tags list for this snipt.
                RebuildSniptTags(resp.tags_list, $('#tags-list-' + id));
                
                // Rebuild the user tags.
                $.getJSON('/tags/list', function(json) {RebuildUserTags(json)});
                
                // If this was a new snipt, handle the addition of the new snipt to the page.
                if (id == 0) {
                    
                    // If this is the very first snipt for a user, show the snipts list, and hide the welcome message.
                    if ($('ul.snipts li').length <= 0) {
                        $('#has-snipts').css('display','block');
                        $('#userpage-content .center').css('display','none');
                    }
                    
                    if (resp.public) {
                        var public_flag = ' style="display: block;"';
                        var key = '';
                    } else {
                        var public_flag = ' style="display: none;"';
                        var key = '?key=' + resp.key;
                    }
                    
                    // Add the new snipt to the snipts list.
                    $('ul.snipts').prepend('' +
                        '<li id="new-' + resp.id + '" class="container-' + resp.id + ' clearfix" style="display: none;">' +
                        '    <span class="description clearfix" id="description-' + resp.id + '"><a title="Permalink for this snipt" href="/' + resp.username + '/' + resp.slug + key + '"><span class="permaslug">&#8734;</span> ' + resp.description + '</a></span>' +
                        '    <pre class="code" id="code-' + resp.id + '" style="display: none;">' + resp.code + '</pre>' +
                        '    <pre class="lexer" id="lexer-raw-' + resp.id + '" style="display: none;">' + resp.lexer + '</pre>' + 
                        '    <p id="public-raw-' + resp.id + '" style="display: none;">' + resp.public + '</p>' +
                        '    <p id="description-raw-' + resp.id + '" style="display: none;">' + resp.description + '</p>' +
                        '    <div id="code-stylized-' + resp.id + '" class="code-stylized"><span id="public-flag-' + resp.id + '" class="public"' + public_flag + '>public</span>' + resp.code_stylized + '</div>' +
                        '    <p class="tools clearfix">' +
                        '        <span class="tools-container">' +
                        '            <a id="copy-' + resp.id + '" href="#" class="right copy">copy</a>' +
                        '            <span class="right separator">|</span>' +
                        '            <a href="#" class="edit right">edit</a>' +
                        '            <span class="right separator embed-' + resp.id + '">|</span>' +
                        '            <a href="#" onclick="$(\'#embed-code-' + resp.id + '\').toggle(); return false;" class="embed right embed-' + resp.id + '">embed</a>' +
                        '        </span>' +
                        '    </p>' +
                        '    <span class="snipt-tags tags-title"><a href="/' + resp.username + '/' + resp.slug + key + '">0 comments</a> - tagged in&nbsp;</span>' +
                        '    <ul class="snipt-tags clearfix" id="tags-list-' + resp.id + '"></ul>' +
                        '    <span class="posted-by tags-title">posted on ' + resp.created_date + ' at ' + resp.created_time + ' EST</span>' +
                        '    <p><input class="tags" name="tags" id="tags-' + resp.id + '" style="display: none;" value="' + resp.tags + '" type="text" /></p>' +
                        '    <p id="embed-code-' + resp.id + '" style="display: none;"><input type="text" class="embed-code right" onclick="$(this).select(); return false;" name="embed-' + resp.id + '" value="&lt;script type=&quot;text/javascript&quot; src=&quot;http://snipt.net/embed/' + resp.key + '&quot;&gt;&lt;/script&gt;" /></p>' +
                        '</li>' +
                    '');
                                        
                    // Rebuild the tags list for this snipt.
                    RebuildSniptTags(resp.tags_list, $('#tags-list-' + resp.id));
                    
                    // Provide visual feedback indicating the instant addition of the snipt to the page.
                    $('ul.snipts li#new-' + resp.id).slideToggle().children('div').children('.highlight').effect("highlight", {color: '#527A9E'}, 750);
                    
                    // Set the add snipt fields' values to blank.
                    $('#description-0').attr('value','');
                    $('#tags-0').attr('value','');
                    
                    // Focus on the code textarea.
                    $('#code-0').attr('value','').focus();
                    
                    // Change the submit links to "add it or i'm done" (instead of cancel).
                    $('.submit').html('<a href="#" onclick="$(\'#submit-new\').click(); return false;">add it</a>&nbsp;&nbsp;or&nbsp;&nbsp;<a class="cancel" href="#" onclick="$(\'#userpage-add-snipt\').slideToggle(); $(this).html(\'cancel\'); return false;">i\'m done</a>');
                }
            }
        });
    }
    return false;
}

function ToggleFav(obj, snipt) {
    $(obj).addClass('loading');
    $.getJSON('/favs/toggle/' + snipt, function(resp) {
        if (resp.favorited == true) {
            $(obj).addClass('favorited')
        } else {
            $(obj).removeClass('favorited')
        }
        $(obj).removeClass('loading')
    });
}
