import React from 'react';

import '../App.css';

import { DrawingCell } from './DrawingCell'


export class DrawingCanvas extends React.Component<Props> {

    state : State;

    constructor(props: any) {
        super(props)
        const cells : boolean[] = Array.from({length: 32 * 32});
        cells.fill(false)
        
        this.state = {
            cells,
            currentlyDrawing : false
        }
    }

    getCells = () => {
        return Array.from(this.state.cells.map(c => c ? 1 : 0))
    }

    dragStart = (e: React.DragEvent<HTMLDivElement>) => {
        this.onMouseDown()
        e.preventDefault();
        e.stopPropagation();
    }

    dragEnd = () => {
        this.onMouseUp()
    }

    onMouseDown = () => {
        this.setState({currentlyDrawing: true})
    }

    onMouseUp = () => {
        this.setState({currentlyDrawing: false})
    }

    clearAll = () => {
        const cells = Array.from({length: 32 * 32})
        cells.fill(false)
        this.setState({ cells })
    }

    updateColor = (number: number, newColor: boolean) => {
        const { cells } = this.state
        const newCells = Array.from(cells)
        newCells[number] = newColor;
        this.setState({ cells: newCells })
    }

    render() {
        return <div className="canvas" 
            onMouseDown={this.onMouseDown} 
            onMouseUp={this.onMouseUp}
            onDragEnter={this.dragStart}
            onDragEnd={this.dragEnd}
            >
            {
                this.state.cells.map((c, i) => 
                <DrawingCell updateColor={this.updateColor} 
                    key={i} 
                    number={i} 
                    value={c} 
                    currentlyDrawing={this.state.currentlyDrawing}></DrawingCell>)
            }
        </div>
    }
}

class Props {}

class State {
    public cells: boolean[] = [];
    public currentlyDrawing = false;
}