import React, { Component } from 'react';

import { Segment, Header } from 'semantic-ui-react'
import CuppingTable from './CuppingTable'


export default class MainContent extends Component {

  handleLoadSession = (session) => {
    console.log(session)
  }

  cuppingsPage() {
    return (
      <CuppingTable handleLoadSession={this.handleLoadSession} />
    )
  }

  newCuppingPage() {
    return (
      <Segment basic>
        <Header as='h3'>New Cupping</Header>
      </Segment>
    )
  }

  render() {
    return (
      <div>
        { this.props.showCuppings ? this.cuppingsPage() : null }
        { this.props.showNewCupping ? this.newCuppingPage() : null }
      </div>
    );
  }

}
