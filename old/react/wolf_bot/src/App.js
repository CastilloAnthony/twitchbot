// @ts-check

import React, {useState, useEffect} from 'react'
import api from './api'

const App = () => {
    const [status, setStatus] = useState([]);
    const [channels, setChannels] = useState([]);
    const [commands, setCommands] = useState([]);
    const [settings, setSettings] = useState ([]);

    const fetchStatus = async() => {
        const response = await api.get('/bot/status');
        setStatus(response.data);
        console.log(response);
    }

    const fetchChannels = async() => {
        const response = await api.get('bot/channels');
        setChannels(response.data);
        console.log(response);
    }

    const fetchCommands = async() => {
        const response = await api.get('bot/commands');
        setCommands(JSON.parse(response.data));
        console.log(response);
    }

    const fetchSettings = async() => {
        const response = await api.get('bot/settings');
        setSettings(JSON.parse(response.data));
        console.log(response);
    }

    useEffect(() => {
        fetchStatus();
        fetchChannels();
        fetchCommands();
        fetchSettings();
    }, []);

    function statusResolver() {
        console.log(status);
        if (status) {
            return 'Online';
        }
        else {
            return 'Offline';
        };
    };

    function channelsResolver() {
        let output = '<ol>';
        for (const element of channels) {
            console.log(element);
            output += '<li>'+element+'</li>';
        };
        output += '</ol>'
        return <div dangerouslySetInnerHTML={{ __html:output }} />
    };

    function commandsResolver() {
        let output = '<ul>';
        Object.keys(commands).forEach(function(key) {
            output += '<div>Name: '+key+'<li>Aliases: <ul>';
            Object.keys(commands[key]).forEach(function(key2) {
                console.log(commands[key][key2])
                if (commands[key][key2] === null) {
                    output += 'N/A';
                }
                else {
                    output += commands[key][key2]+' ';
                };
                
            })
            output += '</ul></li></div></ul>';
        })
        return <div dangerouslySetInnerHTML={{ __html:output }} />
    };

    function settingsResolver() {
        let output = '<ol>';
        Object.keys(settings).forEach(function(key) {
            console.log('Key : ' + key + ', Value : ' + settings[key])
            output += '<li>'+key+': '+settings[key]+'</li>'
        })
        output += '</ol>';
        return <div dangerouslySetInnerHTML={{ __html:output }} />
    };

    return (
        <div>
            <nav className ='navbar navbar-expand-lg navbar-dark bg-primary'>
                <div className='container-fluid'>
                    <a className='navbar-brand' href="/">Wolf Bot</a>
                    <button className='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarNav' aria-controls='navbarNav' aria-expanded='false' aria-label='Toggle navigation'>
                        <span className='navbar-toggler-icon'></span>
                    </button>
                    <div className='collapse navbar-collapse' id='navbarNav'>
                        <ul className='navbar-nav'>
                            <li className='nav-item active'>
                                <a className='nav-link' href='/channels'>Channels</a>
                            </li>
                            <li className='nav-item active'>
                                <a className='nav-link' href='/commands'>Commands</a>
                            </li>
                            <li className='nav-item active'>
                                <a className='nav-link' href='/settings'>Settings</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gridGap: 20 }}>
                <div className='container'>
                    <h2>Bot Status: {statusResolver()}</h2>
                    <h4>Currently Connected Channels:</h4>{channelsResolver()}
                </div>
                <div className='container'><h4>Settings: </h4>{settingsResolver()}</div>
                <div className='container'><h4>Commands: </h4>{commandsResolver()}</div>
            </div>
        </div>
    )
};

export default App;