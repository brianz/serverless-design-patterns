import React, { Component } from 'react';

import { Segment, Header, Grid } from 'semantic-ui-react'
import CuppingTable from './CuppingTable'

import './css/index.css'

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
      <Grid id="main-content">
        <Grid.Row className="main-content-wrapper">
          <Grid.Column width={14}>
            { this.props.showCuppings ? this.cuppingsPage() : null }
            { this.props.showNewCupping ? this.newCuppingPage() : null }
          </Grid.Column>
        </Grid.Row>
      </Grid>
    );
  }

}
