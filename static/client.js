var View = function(table, params){
    var x = params.x || 0;
    var y = params.y || 0;
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
        if(pos<(offset+margin)){
            if((pos-margin)>0){
                return pos-margin;
            }else{
                return 0;
            }
        };
        if(pos>((offset+size)-(margin+1))){
            console.log('mm',max,size,(max-size));
            if(pos-(size-(margin+1))>(max-size)){
                return max-size;
            }else{
                return pos-(size-(margin+1));
            }
        };
        return offset;
    };
    this.update = function(maze, avatar){
        // Update view using maze with avatar location
        var ma = maze.array;
        x = align_dimension(avatar.x, maze.width, x, width, margin);
        y = align_dimension(avatar.y, maze.height, y, height, margin);
        console.log('view x,y:',x,y);
        console.log('avatar view x,y:',avatar.x,avatar.y);
        for(var vx=x;vx<(x+width);vx++){
            for(var vy=y;vy<(y+height);vy++){
                var mt = ma[vx][vy];
                jQuery('#'+(vx-x)+'-'+(vy-y)).attr('class', mt);
            };
        };
        jQuery('#'+(avatar.x-x)+'-'+(avatar.y-y)).attr('class', 'avatar');

        console.log('view max x,y:',vx,vy);
    };
};


var Maze = function(width, height){
    var maze_array = [];
    // FIXME var naming
    for(line_no=0;line_no<width;line_no++){
        var line = [];
        for(col_no=0;col_no<height;col_no++){
            line[col_no] = 'wall';
        };
        maze_array[line_no] = line;
    };
    this.update_tiles = function(tiles){
        for(tile_no in tiles){
            tile = tiles[tile_no];
            maze_array[tile.x][tile.y] = 'clear';
        };
    };
    this.get_tiles = function(x,y,width,height){
        var ret = [];
        for(col_no=x;col_no<(x+width);col_no++){
            var col = [];
            for(line_no=y;line_no<(y+height);line_no++){
                col.push(maze_array[col_no][line_no]);
            };
            ret.push(col);
        };
        return ret
    };
    this.array = maze_array;
    this.width = width;
    this.height = height;
}

var clear_tiles = function(tiles){
    var shade_tile = function(x,y){
        var shade_jqo = jQuery('#'+x+'-'+y);
        if(shade_jqo.length == 1){
            var shade_class = shade_jqo.attr('class');
            if(shade_class == 'wall') shade_jqo.attr('class','shade');
        }
    };
    for(tile_no in tiles){
        tile = tiles[tile_no];
        var selector = '#'+tile.x+'-'+tile.y;
        var tile_jqo = jQuery(selector);
        var tile_class = tile_jqo.attr('class');
        if(tile_class != 'clear'){ // Skip any we have already cleared
            tile_jqo.attr('class', 'clear');
            /*
            if(tile.shape & 1){ shade_tile(tile.x,tile.y-1); }
            if(tile.shape & 2){ shade_tile(tile.x+1,tile.y); }
            if(tile.shape & 4){ shade_tile(tile.x,tile.y+1); }
            if(tile.shape & 8){ shade_tile(tile.x-1,tile.y); }
            */
        }
    }
};

var paint_movers = function(json,cls){
    if(!cls){cls='avatar'};
    if(json.avatar){
        var selector = '#'+json.avatar.x+'-'+json.avatar.y;
        jQuery(selector).attr('class',cls);
    }
    if(json.others){
        if(cls=='avatar'){cls='other'};
        for(other_no in json.others){
            var other = json.others[other_no];
            var selector = '#'+other.x+'-'+other.y;
            jQuery(selector).attr('class',cls);
        }
    }
};

var handle_update = function(){
    var last_run = 'first_run';
    return function(json){

        if(last_run=='first_run'){
            //make_maze(json.maze.width, json.maze.height);
            //make_maze(20,20);
        }
        m.update_tiles(json.tiles);
        v.update(m,json.avatar);
        //clear_tiles(json.tiles);

        //paint_movers(last_run,'clear');
        //paint_movers(json);
        last_run = json;
    }
}();

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
        case 74: //j
            move_avatar(8);
            break;
        case 39: // Right
        case 68: //d
        case 76: //l
            move_avatar(2);
            break;
        case 40: // Down
        case 83: // s
        case 75: //k
            move_avatar(4);
            break;
    }
};

var get_name = function(){
    var name_regex = new RegExp("[\\?&]name=([^&#]*)");
    var match = name_regex.exec(window.location.href);
    if(match==null){
        return null;
    }else{
        return match[1];
    }
}

var move_avatar = function(direction){
    jQuery.post(pos_url,{move:direction},handle_update,'json');
};
