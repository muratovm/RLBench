import logo from './logo.svg';
import './App.css';
import React from 'react';

function randomChoice(p) {
  let rnd = p.reduce( (a, b) => a + b ) * Math.random();
  return p.findIndex( a => (rnd -= a) < 0 );
}

function randomChoices(p, count) {
  return Array.from(Array(count), randomChoice.bind(null, p));
}

class State{

  constructor(name, reward){
    this.name = name
    this.value = 0
    this.reward = reward
    this.neighbors = []
    this.p_transitions = []
  }
  
  next_state() {
    var total = this.p_transitions.reduce(function(a, b){return a + b;}, 0);
    var p_transitions = this.p_transitions
    for(let i =0; i < this.p_transitions.length; i++){
      p_transitions[i] /= total
    }
    var index = randomChoices(p_transitions, 1);
    var choice = this.neighbors[index]
    
    var p_index = this.neighbors.indexOf(choice);
    var prob = this.p_transitions[p_index];
    return [choice, prob]
  }
  
  add_neighbor(neighbor, probablility){
    this.neighbors.push(neighbor)
    this.p_transitions.push(probablility)
  }
  
}

function States(props) {
  const cells = []
  var values = props.states.map( (state) => state.value)
  var maximum = Math.max(...values)

  if(maximum==0){maximum=1}

  //let result = randomChoices([0.3, 0.3, 0.4], 1);
  //console.log(result);

  for (const [index, state] of props.states.entries()) {
    //const random_color = "#" + String(Math.floor(Math.random()*16777215).toString(16));
    var value = state.value
    var rgb = [255*(value/maximum),255*(value/maximum),255*(value/maximum)]

    const background = "rgb("+rgb[0]+","+ rgb[1]+","+ rgb[2]+")";
    
    var text = "rgb(255,0,0)"
    if(rgb[0] < 125){text = "rgb(255,255,255)";}
    else{text = "rgb(0,0,0)";}
    cells.push(<Cell key={index+1} value={value} reward={state.reward} background={background} color={text}/>)
  }
  return (<div className="container">{cells}</div>
  );
}

function Cell(props){

  var value = props.value.toFixed(2);
  return (
    <div className="cell">
        <div className="square" style={{"background-color": props.background}} >
            <div className="label_text" style={{"color":props.color}}>{props.reward}</div>
            <div className="value_text" style={{"color":props.color}}>{value}</div>
        </div>
    </div>
  );
}

class MarovStates extends React.Component{

  constructor(props) {
    super(props);
    this.state = {date: new Date(),
                  tick: 0};

    this.agent_rewards = 0

    var s1 = new State(0, 1)
    var s2 = new State(1, 0)
    var s3 = new State(2, 0)
    var s4 = new State(3, 5)
    var s5 = new State(4, 0)
    var s6 = new State(5, 0)
    var s7 = new State(6, 10)

    s1.add_neighbor(s1.name, 0.6)
    s1.add_neighbor(s2.name, 0.4)

    s2.add_neighbor(s1.name, 0.4)
    s2.add_neighbor(s2.name, 0.2)
    s2.add_neighbor(s3.name, 0.4)

    s3.add_neighbor(s2.name, 0.4)
    s3.add_neighbor(s3.name, 0.2)
    s3.add_neighbor(s4.name, 0.4)

    s4.add_neighbor(s3.name, 0.4)
    s4.add_neighbor(s4.name, 0.2)
    s4.add_neighbor(s5.name, 0.4)

    s5.add_neighbor(s4.name, 0.4)
    s5.add_neighbor(s5.name, 0.2)
    s5.add_neighbor(s6.name, 0.4)
            
    s6.add_neighbor(s5.name, 0.4)
    s6.add_neighbor(s6.name, 0.2)
    s6.add_neighbor(s7.name, 0.4)

    s7.add_neighbor(s6.name, 0.4)
    s7.add_neighbor(s7.name, 0.6)
    
    this.states = [s1,s2,s3,s4,s5,s6,s7]
    this.current_name = 4
    this.gamma = props.gamma
  }

  find_values_agent(){
    var [new_name,prob] = this.states[this.current_name].next_state()
    this.states[new_name].value += this.gamma * (this.states[new_name].reward - this.states[new_name].value)
    this.current_name = this.states[new_name].name
  }

  blind_agent(){
    var [new_name,prob] = this.states[this.current_name].next_state()
    var value_choice = prob * (this.states[new_name].reward + this.gamma * this.states[new_name].value)
    var value_other = (1-prob) * ( this.gamma * this.states[this.current_name].value)
    //update current state
    this.states[this.current_name].value = (value_choice + value_other)
    this.current_name = this.states[new_name].name
  }

  aware_agent(){
    var current_value = 0;
    for(let i = 0; i < this.states[this.current_name].neighbors.length; i++){
        var neighbor = this.states[this.current_name].neighbors[i]
        var prob = this.states[this.current_name].p_transitions[i]
        var value = this.states[neighbor].value
        var reward = this.states[neighbor].reward
        current_value += prob*(reward + (this.gamma*value))
    }
    this.states[this.current_name].value = current_value
    var [new_name,prob] = this.states[this.current_name].next_state()
    this.current_name = this.states[new_name].name
  }

  step(){
    this.blind_agent()
    //this.aware_agent()
    this.agent_rewards += this.states[this.current_name].reward
    return this.states[this.current_name]
  }

  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      100
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({
      date: new Date(),
      tick: this.state.tick+1
    });

    const max = 10;
    const min = 0;
    this.step()
    /*
    for (let i = 0; i < this.state.values.length; i++) {
      this.state.values[i] = Math.floor(Math.random() * (max - min + 1)) + min;
    }
    */
    console.log("tick")
  }

  myStopFunction() {
    clearInterval(this.timerID);
  }


  render() {
    return (
      <div>
        <States states={this.states}/>
      </div>
    );
  }
}

export default MarovStates;
