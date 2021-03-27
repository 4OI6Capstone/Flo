import logo from './logo.svg';
import Flo_Logo from './Flo_Logo.png'
import './App.css';
import React, {Component} from "react";
import Dropzone from "react-dropzone"
import { render } from "react-dom"
import { Button } from '@material-ui/core';
import ReactLoading from 'react-loading';
import ReactAudioPlayer from 'react-audio-player'
import TextLoop from 'react-text-loop'

const host = 'http://localhost';
const port = ':8080';
const endPoint = '/get-mix';
const loadingMessages = ["Yes we know it's taking long", "Just a little longer", 
"Go get a coffee", "Might be done by the time you check again", "Upgrades coming soon™", 
"This is still working don't worry", "Please wait still loading", "Brought to you by Flo."];


class App extends Component {
  constructor() {
    super();
    this.state = {
      files : [],
      finalMix : '',
      loading: false,
      error: false,
      errorMessage: ''
    }
    this.generateMix = this.generateMix.bind(this);
    this.addFile = this.addFile.bind(this);
  }

  generateMix() {
    var data = new FormData();
    for (let i = 0; i < this.state.files.length; i++) {
      data.append("files", this.state.files[i]);
    }
    const requestOptions = {
      method: 'POST',
      body: data
    };
    this.setState({
      loading: true,
    })
    const url = host+port+endPoint;
    fetch(url, requestOptions)
    .then(response =>  response.blob())
    .then(audioBlob => {
      var objectURL = URL.createObjectURL(audioBlob);
      this.setState({
        finalMix: objectURL,
        loading: false
      })
    })
    .catch(error => {
      this.setState({
            error: true,
            error: error
      });
      throw new Error('Something went wrong');
    }
  )};

  addFile(files) {
    for(var i = 0; i < files.length; i++) {
      this.setState(prevState => ({
        files : [...this.state.files, files[i]],
      }))
    }
  }

  render() {
    let currentSrc = this.state.finalMix
    return (
      <div className="App">
      <header className="App-header">
        <img src={Flo_Logo} className="App-logo" alt="logo" />
        <h1>
          Flo. : The Automated Song Mixer.
        </h1>
        <Dropzone onDrop={acceptedFiles => this.addFile(acceptedFiles)}>
          {({getRootProps, getInputProps}) => (
            <section>
              <div {...getRootProps()} className="Drop-box">
                <input {...getInputProps()} />
                {this.state.files.length === 0 ? (
                <p>Drag 'n' drop Songs here, or click to select Song files</p>) : (
                <p> Current files in mix:</p>)}
                {this.state.files.map( file => (
                    <p key={file.name} className="song-list">
                      {file.name}
                    </p>
                ))}
              </div>
            </section>
          )}
        </Dropzone>
        <div className = "Submit-button">
          <Button
            variant="contained" color="primary" component="span" 
            onClick={() => this.generateMix()}
          >
            Generate Mix
          </Button>   
        </div>
        {this.state.loading ? (
          <>{<ReactLoading type='spinningBubbles' color='white' width='100px' height='100px' className='loading'/>}
          {<TextLoop children={loadingMessages} interval={3000} springConfig={{ stiffness: 180, damping: 8 }}/> }</>)
        : null}
        {currentSrc != '' ? (
          <ReactAudioPlayer src={currentSrc} autoPlay controls className="music-player" /> 
        ): null}
        {this.state.error == true ? (
          <p>Oops an error occured: {}</p>
        ): null}
      </header>
    </div>
    )
  }
};

export default App;
