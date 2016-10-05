/*var CharNode = React.createClass({
    render : function(){
        return (
       </br>
        );
    }
})*/
var CharList = React.createClass({
 render : function(){
    var CharElements = this.props.data.map(function(char){
        return (
            <img src={char.image_url} key={char.id}></img>
        );
    })
    return (
        <div>
            <p>hello!{this.props.name} </p>
            {CharElements}
        </div>
    );
}
})

var CharArea = React.createClass({
    getInitialState: function(){
        return {data:[
        ]};
    },
    componentDidMount: function(){
        //this.setState({data:data});
         $.ajax({
          url: this.props.url,
          dataType: 'json',
          cache: false,
          success: function(data) {
            this.setState({data: data.models});
          }.bind(this),
          error: function(xhr, status, err) {
            console.log('error');
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    },
    render: function(){
        return(
        <div>
            <CharList name='xq' data={this.state.data}/>
        </div>

        );
    }
})

