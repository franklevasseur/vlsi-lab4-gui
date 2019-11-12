import React, { RefObject } from 'react';
import classnames from 'classnames';

import '../App.css';

export class DrawingCell extends React.Component<Props> {

    state = {
        isColored : false,
        number: 0,
        currentlyDrawing: false
    }

    componentDidMount = () => {
        if (!this.props) {
            return;
        }
        const { number, value } = this.props;
        this.setState({ number, isColored: value })
    }

    componentDidUpdate = (prevProps: Props) => {
        if (prevProps.value === this.props.value) {
            return
        }

        const { value } = this.props;
        this.setState({ isColored: value })
    }

    handleMouseEnter = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.currentlyDrawing) {
            this.color();
        }
    }

    handleClick = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        this.toggleColor();
    }

    toggleColor = () => {
        const isColored = !(this.state.isColored);
        this.setState({ isColored })
        this.props.updateColor(this.props.number, isColored)
    }

    color = () => {
        this.setState({ isColored: true })
        this.props.updateColor(this.props.number, true)
    }

    render() {
        return <div 
            onMouseEnter={this.handleMouseEnter}
            onClick={this.handleClick}
            onSelect={e => console.log("selection")}
            className={classnames("cell", this.state.isColored ? "active-cell" : "inactive-cell")} />
    }
}

class Props {
    number : number;
    value : boolean;
    currentlyDrawing : boolean;
    updateColor : (number: number, newColor: boolean) => void
}