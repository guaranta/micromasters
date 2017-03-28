// @flow
import { createAction } from 'redux-actions';
import type { Dispatch } from 'redux';
import R from 'ramda';

import type { Action, ActionType, Dispatcher } from '../flow/reduxTypes';
import type { Endpoint, RestState } from '../flow/restTypes';
import { fetchJSONWithCSRF } from './api';
import {
  FETCH_PROCESSING,
  FETCH_SUCCESS,
  FETCH_FAILURE,
} from '../actions';
import { GET, PATCH, POST } from '../constants';
import { couponEndpoint } from '../reducers/coupons';

const actionize = R.compose(R.toUpper, R.join("_"));

export const requestActionType = (...xs: string[]) => `REQUEST_${actionize(xs)}`;

export const successActionType = (...xs: string[]) => `RECEIVE_${actionize(xs)}_SUCCESS`;

export const failureActionType = (...xs: string[]) => `RECEIVE_${actionize(xs)}_FAILURE`;

export const clearActionType = (...xs: string[]) => `CLEAR_${actionize(xs)}`;

export const INITIAL_STATE: RestState = {
  loaded: false,
  processing: false,
};

const defaultRESTPrefixes = { GET, PATCH, POST };

const getPrefixForEndpoint = (verb, endpoint) => (
  R.propOr(defaultRESTPrefixes[verb], `${R.toLower(verb)}Prefix`, endpoint)
);

export function makeFetchFunc(endpoint: Endpoint): (...args: any) => Promise<*> {
  return (...args) => fetchJSONWithCSRF(endpoint.url, endpoint.makeOptions(...args));
}

type DerivedAction = {
  action:       (...params: any) => Dispatcher<*>,
  requestType:  ActionType,
  successType:  ActionType,
  failureType:  ActionType,
};

// we can derive an action from an Endpoint object and an HTTP verb 
// this returns an object containing the derived REST action (which
// is an async action suitable for use with redux-thunk), and all the
// derived action types.
export const deriveAction = (endpoint: Endpoint, verb: string): DerivedAction => {
  const prefix = getPrefixForEndpoint(verb, endpoint);

  const requestType = requestActionType(prefix, endpoint.name);
  const successType = successActionType(prefix, endpoint.name);
  const failureType = failureActionType(prefix, endpoint.name);

  const requestAction = createAction(requestType);
  const successAction = createAction(successType);
  const failureAction = createAction(failureType);

  const fetchFunc = R.propOr(
    makeFetchFunc(endpoint),
    `${R.toLower(verb)}Func`,
    endpoint
  );

  return {
    action: (...params) => {
      return (dispatch: Dispatch): Promise<*> => {
        dispatch(requestAction());
        return fetchFunc(...params).then(data => {
          dispatch(successAction(data));
          return Promise.resolve(data);
        }).catch(error => {
          dispatch(failureAction(error));
          return Promise.reject(error);
        });
      };
    },
    requestType, successType, failureType
  };
};

// here we loop through the HTTP verbs that an Endpoint implements, and
// for each one we derive an action. The derived action types are stuck on
// the function object, as a convenience.
export const deriveActions = (endpoint: Endpoint) => {
  let actions = {};
  endpoint.verbs.forEach(verb => {
    const {
      action,
      requestType,
      successType,
      failureType,
    } = deriveAction(endpoint, verb);

    let lverb = R.toLower(verb);

    actions[lverb] = action;
    actions[lverb].requestType = requestType;
    actions[lverb].successType = successType;
    actions[lverb].failureType = failureType;
  });
  let clearType = clearActionType(endpoint.name);
  actions.clearType = clearType;
  actions.clear = createAction(clearType);
  return actions;
};

// a reducer may be derived on the basis of an Endpoint object, an already
// derived REST action, and an HTTP verb
// A reducer, in this case, is an Object<type, Function>, where type is an
// action type defined on the previously derived action, and the Function has
// the type State -> Action -> State
//
// so the type of the function overall could be rendered
// deriveReducer :: Endpoint -> Action -> String -> Object String (State -> Action -> State)
export const deriveReducer = (endpoint: Endpoint, action: Function, verb: string) => {
  let fetchStatus = `${R.toLower(verb)}Status`;

  return {
    [action.requestType]: (state: Object, action: Action<any, any>) => ({
      ...state,
      [fetchStatus]: FETCH_PROCESSING,
      loaded: false,
      processing: true,
    }),
    [action.successType]: (state: Object, action: Action<any, any>) => ({
      ...state,
      [fetchStatus]: FETCH_SUCCESS,
      data: action.payload,
      loaded: true,
      processing: false,
    }),
    [action.failureType]: (state: Object, action: Action<any, any>) => ({
      ...state,
      [fetchStatus]: FETCH_FAILURE,
      error: action.payload,
      loaded: true,
      processing: false,
    }),
  };
};

export const deriveReducers = (endpoint: Endpoint, actions: Function) => {
  let initialState = R.propOr(INITIAL_STATE, 'initialState', endpoint);

  const reducers = R.reduce(R.merge, {}, [
    ...endpoint.verbs.map(verb => deriveReducer(endpoint, actions[R.toLower(verb)], verb)),
    R.propOr({}, 'extraActions', endpoint),
    { [actions.clearType]: () => initialState},
  ]);

  return (state: Object = initialState, action: Action<any, any>) => (
    R.has(action.type, reducers) ? reducers[action.type](state, action) : state
  );
};

export const endpoints: Array<Endpoint> = [
  couponEndpoint,
];

const reducers: Object = {};
const actions: Object = {};
endpoints.forEach(endpoint => {
  actions[endpoint.name] = deriveActions(endpoint);
  reducers[endpoint.name] = deriveReducers(endpoint, actions[endpoint.name]);
});

export { reducers, actions };