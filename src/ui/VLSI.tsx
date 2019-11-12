import React, { RefObject } from 'react';
import * as axios from 'axios';

import { DrawingCanvas } from './DrawingCanvas'

export class VLSI extends React.Component {

    child: RefObject<DrawingCanvas> = React.createRef();

    sendDrawing = () => {
        const config : axios.AxiosRequestConfig = {}
        config.headers = {
            'Content-Type': 'application/json'
        }

        const data = JSON.stringify(this.child.current.getCells())

        axios.default.post(`${window.location.origin.toString()}/pattern`, data, config).then(t => {
            console.log("succes...")
        })
    }

    eraseAll = () => {
        (this.child.current || {clearAll: () => {}}).clearAll();
    }

    render() {
        return <div>
            <div className="header">
                <button onClick={this.sendDrawing} className="action">Envoyer</button>
                <button onClick={this.eraseAll} className="action">Effacer tout</button>
                <button className="action">Rien</button>
            </div>
            <DrawingCanvas ref={this.child}/>
        </div>
    }
}