// @flow
/* global SETTINGS: false */
import React from 'react';
import { connect } from 'react-redux';
import Loader from '../components/Loader';
import R from 'ramda';
import DocumentTitle from 'react-document-title';

import { FETCH_PROCESSING, FETCH_SUCCESS, FETCH_FAILURE } from '../actions';
import { clearProfile } from '../actions/profile';
import {
  profileFormContainer,
  mapStateToProfileProps,
  childrenWithProps,
} from './ProfileFormContainer';
import ErrorMessage from '../components/ErrorMessage';
import { fetchDashboard } from '../actions/dashboard';
import { hasAnyStaffRole } from '../lib/roles';
import { getDashboard } from '../reducers/util';
import { S } from '../lib/sanctuary';
import { LEARNER_EMAIL_TYPE } from '../components/email/constants';
import { LEARNER_EMAIL_CONFIG } from '../components/email/lib';
import { withEmailDialog } from '../components/email/hoc';
import type { ProfileContainerProps } from './ProfileFormContainer';
import type { DashboardsState } from '../flow/dashboardTypes';
import type { AllEmailsState } from '../flow/emailTypes';
import { showDialog, hideDialog } from '../actions/ui';
import { GRADE_DETAIL_DIALOG } from '../constants';

const notFetchingOrFetched = R.compose(
  R.not, R.contains(R.__, [FETCH_PROCESSING, FETCH_SUCCESS, FETCH_FAILURE])
);

type LearnerPageProps = ProfileContainerProps & {
  dashboard: DashboardsState,
  email: AllEmailsState,
  openEmailComposer: (emailType: string, emailOpenParams: any) => void,
};

class LearnerPage extends React.Component<*, LearnerPageProps, *> {
  componentDidMount() {
    const { params: { username }, fetchProfile } = this.props;
    fetchProfile(username);
    this.fetchDashboard();
  }

  componentDidUpdate() {
    const { params: { username }, fetchProfile } = this.props;
    fetchProfile(username);
    this.fetchDashboard();
  }

  componentWillUnmount() {
    const { dispatch, params: { username } } = this.props;
    if (!SETTINGS.user || SETTINGS.user.username !== username) {
      // don't erase the user's own profile from the state
      dispatch(clearProfile(username));
    }
  }

  getFocusedDashboard() {
    const { dashboard, params: { username }} = this.props;
    return S.filter(
      () => hasAnyStaffRole(SETTINGS.roles),
      getDashboard(username, dashboard)
    );
  }

  fetchDashboard() {
    const { dispatch, params: { username } } = this.props;

    R.compose(
      S.map(() => dispatch(fetchDashboard(username))),
      S.filter(R.propSatisfies(notFetchingOrFetched, 'fetchStatus'))
    )(this.getFocusedDashboard());
  }

  getDocumentTitle = () => {
    const {
      params: { username },
      profiles,
    } = this.props;
    let profilePath = [username, 'profile'];

    let name = R.pathOr('', profilePath.concat('preferred_name'), profiles);

    return `${name} | MITx MicroMasters Profile`
      .trim()
      .replace(/^\|\s/, '');
  }

  setShowGradeDetailDialog = (open: boolean, courseTitle: string) => {
    const { dispatch } = this.props;
    if (open) {
      dispatch(showDialog(`${GRADE_DETAIL_DIALOG}${courseTitle}`));
    } else {
      dispatch(hideDialog(`${GRADE_DETAIL_DIALOG}${courseTitle}`));
    }
  };

  render() {
    const {
      params: { username },
      profiles,
      children,
      profileProps,
      email,
      openEmailComposer
    } = this.props;

    let profile = {};
    let toRender = null;
    let loaded = false;
    if (profiles[username] !== undefined) {
      profile = profiles[username];
      loaded = profiles[username].getStatus !== FETCH_PROCESSING;
      let props = {
        dashboard: S.maybe({}, R.identity, this.getFocusedDashboard()),
        email: email,
        openLearnerEmailComposer: R.partial(openEmailComposer(LEARNER_EMAIL_TYPE), [profile.profile]),
        setShowGradeDetailDialog: this.setShowGradeDetailDialog,
        ...profileProps(profile)
      };
      toRender = childrenWithProps(children, props);
    }
    const { errorInfo } = profile;
    return (
      <DocumentTitle title={this.getDocumentTitle()}>
        <Loader loaded={loaded}>
          {errorInfo && loaded ? <ErrorMessage errorInfo={errorInfo} /> : toRender }
        </Loader>
      </DocumentTitle>
    );
  }
}

const mapStateToProps = state => {
  return {
    dashboard: state.dashboard,
    email: state.email,
    ...mapStateToProfileProps(state),
  };
};

export default R.compose(
  connect(mapStateToProps),
  withEmailDialog({
    [LEARNER_EMAIL_TYPE]: LEARNER_EMAIL_CONFIG
  }),
  profileFormContainer
)(LearnerPage);
