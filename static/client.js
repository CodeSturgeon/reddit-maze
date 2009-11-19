var View = function(table, params){
    // CSS viewport window for displaying mazes (based on table)
    var x = params.x || -1;
    var y = params.y || -1;
    var ax = params.x || -1;
    var ay = params.y || -1;
    var margin = params.margin || 3; // Number of tiles to keep on edges
    var width = params.width || 10;
    var height = params.height || 10;
    var setup = function(width, height, indexes){
        // Setup the view table
        var tab = table;

        var num_row = document.createElement('tr');
        num_row.appendChild(document.createElement('td'));
        for(lop=0;lop<width;lop++){
            var new_cell = document.createElement('th');
            var num = lop.toString(10);
            if(num.length == 1){
                new_cell.appendChild(document.createTextNode((lop+'')[0]));
            } else {
                new_cell.className = 'ddiget';
                new_cell.appendChild(document.createTextNode(num[0]));
                new_cell.appendChild(document.createElement('br'));
                new_cell.appendChild(document.createTextNode(num[1]));
            }
            num_row.appendChild(new_cell);
        }
        num_row.appendChild(document.createElement('td'));
        
        if(indexes){
        // Head row
            tab.appendChild(num_row);
        }

        for(lop=0;lop<height;lop++){
            var body_row = document.createElement('tr');
            if(indexes){
                var num_cell = document.createElement('th');
                num_cell.appendChild(document.createTextNode(lop.toString(10)));
                body_row.appendChild(num_cell);
            }
            for(lop2=0;lop2<width;lop2++){
                var new_cell = document.createElement('td');
                new_cell.className = 'wall';
                new_cell.id = lop2+'-'+lop;
                new_cell.appendChild(document.createTextNode(' '));
                body_row.appendChild(new_cell);
            }
            if(indexes){
                body_row.appendChild(num_cell.cloneNode(true));
            }
            tab.appendChild(body_row);
        }

        // Foot row
        if(indexes){
            tab.appendChild(num_row.cloneNode(true));
        }
    }(width,height);
    var align_dimension = function(pos, max, offset, size, margin){
        // Align a view window along an axis
        // For a given postision (pos) along axis ranged from 0 to (max)
        // Position a window of length (size), (offset) from 0 along the axis
        // Try to maintain (margin) units from (pos)
        if(pos<(offset+margin)){
            if((pos-margin)>0){
                return pos-margin;
            }else{
                return 0;
            }
        }
        if(pos>((offset+size)-(margin+1))){
            if(pos-(size-(margin+1))>(max-size)){
                return max-size;
            }else{
                return pos-(size-(margin+1));
            }
        }
        if(offset===-1){
            return 0;
        }
        return offset;
    };
    this.paint = function(maze){
        // Update view using maze
        var ma = maze.array;
        for(var vx=x;vx<(x+width);vx++){
            for(var vy=y;vy<(y+height);vy++){
                var mt = ma[vx][vy];
                jQuery('#'+(vx-x)+'-'+(vy-y)).attr('class', mt);
            }
        }
        jQuery('#'+(ax-x)+'-'+(ay-y)).attr('class', 'avatar');
    }
    this.move_avatar = function(maze, avatar){
        // Update view using maze with avatar location
        var ma = maze.array;
        if(ax!==-1){
            jQuery('#'+(ax-x)+'-'+(ay-y)).attr('class', 'trail');
        }
        ax = avatar.x;
        ay = avatar.y;
        ma[avatar.x][avatar.y] = 'trail';
        var nx = align_dimension(ax, maze.width, x, width, margin);
        var ny = align_dimension(ay, maze.height, y, height, margin);
        if(nx!==x || ny!==y){
            x = nx;
            y = ny;
            this.paint(maze);
        }
        jQuery('#'+(ax-x)+'-'+(ay-y)).attr('class', 'avatar');
    }
}


var Maze = function(width, height){
    // Virtual map of the known and unknown tiles on in a maze
    var maze_array = [];
    // FIXME var naming
    for(line_no=0;line_no<width;line_no++){
        var line = [];
        for(col_no=0;col_no<height;col_no++){
            line[col_no] = 'unknown';
        }
        maze_array[line_no] = line;
    }
    this.update_tiles = function(tiles){
        for(tile_no in tiles){
            tile = tiles[tile_no];
            var c = maze_array[tile.x][tile.y];
            if(c!=='clear'&&c!=='trail'){
                maze_array[tile.x][tile.y] = 'clear';
                if(tile.x>0){
                    var c = maze_array[tile.x-1][tile.y];
                    if(c==='unknown'){
                        if(tile.shape & 8){
                            maze_array[tile.x-1][tile.y] = 'shade';
                        }else{
                            maze_array[tile.x-1][tile.y] = 'wall';
                        }
                    }
                }
                if(tile.x<width){
                    var c = maze_array[tile.x+1][tile.y];
                    if(c==='unknown'){
                        if(tile.shape & 2){
                            maze_array[tile.x+1][tile.y] = 'shade';
                        }else{
                            maze_array[tile.x+1][tile.y] = 'wall';
                        }
                    }
                }
                if(tile.y>0){
                    var c = maze_array[tile.x][tile.y-1];
                    if(c==='unknown'){
                        if(tile.shape & 1){
                            maze_array[tile.x][tile.y-1] = 'shade';
                        }else{
                            maze_array[tile.x][tile.y-1] = 'wall';
                        }
                    }
                }
                if(tile.x<height){
                    var c = maze_array[tile.x][tile.y+1];
                    if(c==='unknown'){
                        if(tile.shape & 4){
                            maze_array[tile.x][tile.y+1] = 'shade';
                        }else{
                            maze_array[tile.x][tile.y+1] = 'wall';
                        }
                    }
                }
            }
        }
    }
    this.get_tiles = function(x,y,width,height){
        var ret = [];
        for(col_no=x;col_no<(x+width);col_no++){
            var col = [];
            for(line_no=y;line_no<(y+height);line_no++){
                col.push(maze_array[col_no][line_no]);
            }
            ret.push(col);
        }
        return ret;
    }
    this.array = maze_array;
    this.width = width;
    this.height = height;
}

var move_element_clicker = function(event){ move_avatar(event.target.value); };

var key_handler = function(event){
    switch(event.keyCode){
        case 38: // Up Arrow
        case 87: // w
        case 73: // i
            move_avatar(1);
            break;
        case 37: // Left Arrow
        case 65: // a
        case 74: // j
            move_avatar(8);
            break;
        case 39: // Right
        case 68: // d
        case 76: // l
            move_avatar(2);
            break;
        case 40: // Down
        case 83: // s
        case 75: // k
            move_avatar(4);
            break;
    }
}

var get_qvar = function(name){
    // Get a variable (name) from querystring
    var name_regex = new RegExp("[\\?&]"+name+"=([^&#]*)");
    var match = name_regex.exec(window.location.href);
    if(match===null){
        return null;
    }
    return match[1];
}

var nomove = false;
var avatar_pos = null;

var first_get = function(json){
    avatar_pos = json.avatar;
    m.update_tiles(json.tiles);
    v.move_avatar(m,json.avatar);
}

var handle_update = function(json){
    // FIXME graceful null handling for seen=1
    m.update_tiles(json.tiles);
    v.paint(m);
}

var unblocker = function(){
    nomove = false;
    if(move_list.length>0){
        moveit();
    }
}

var vectors = {1:[0,-1],2:[1,0],4:[0,1],8:[-1,0]};

var move_list = [];

var move_avatar = function(direction){
    var move_data = {move:direction};
    var dv = vectors[direction];
    var nx = avatar_pos.x + dv[0];
    var ny = avatar_pos.y + dv[1];
    var mt = m.array[nx][ny];
    if(mt==='trail' || mt==='clear' || mt==='shade'){
        if(mt==='trail'){
            move_data['seen'] = 1;
        }
        avatar_pos.x = nx;
        avatar_pos.y = ny;
        avatar_pos.moves += 1;
        move_data['move_lock'] = avatar_pos.moves;
        v.move_avatar(m,avatar_pos);
        move_list.push(move_data);
        moveit();
    }
}

var moveit = function(){
    if(nomove) return;
    nomove = true;
    var move_data = JSON.stringify({'moves':move_list});
    move_list = [];
    var ajax_cfg = {'url': pos_url, type:'POST', data: move_data,
            complete: unblocker, success: handle_update, dataType:'json',
            contentType:'application/json', processData: false,
            error:function(XHR, tst, err){alert(XHR.responseText)} };
    jQuery.ajax(ajax_cfg);
}
