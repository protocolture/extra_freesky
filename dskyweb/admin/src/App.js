import React, { useState } from 'react';
import './App.css';

function App() {
    const [key, setKey] = useState('');
    const [value, setValue] = useState('');
    const [result, setResult] = useState('');

    const handleSet = () => {
        fetch(`http://192.168.20.71:7379/SET/${key}/${value}`)
            .then(response => response.json())
            .then(data => {
                setResult(data.SET);
            });
    };

    const handleGet = () => {
        fetch(`http://192.168.20.71:7379/GET/${key}`)
            .then(response => response.json())
            .then(data => {
                setResult(data.GET);
            });
    };

    const handleExists = () => {
        fetch(`http://192.168.20.71:7379/EXISTS/${key}`)
            .then(response => response.json())
            .then(data => {
                setResult(data.EXISTS ? 'Exists' : 'Does not exist');
            });
    };

    return (
        <div className="App">
            <div>
                <label>
                    Key:
                    <input value={key} onChange={(e) => setKey(e.target.value)} />
                </label>
                <label>
                    Value:
                    <input value={value} onChange={(e) => setValue(e.target.value)} />
                </label>
            </div>
            <div>
                <button onClick={handleSet}>SET</button>
                <button onClick={handleGet}>GET</button>
                <button onClick={handleExists}>EXISTS</button>
            </div>
            <div>
                <h3>Result:</h3>
                <p>{result}</p>
            </div>
        </div>
    );
}

export default App;
