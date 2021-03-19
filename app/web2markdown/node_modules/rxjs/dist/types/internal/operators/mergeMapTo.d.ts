import { OperatorFunction, ObservedValueOf, ObservableInput } from '../types';
export declare function mergeMapTo<O extends ObservableInput<unknown>>(innerObservable: O, concurrent?: number): OperatorFunction<any, ObservedValueOf<O>>;
/** @deprecated */
export declare function mergeMapTo<T, R, O extends ObservableInput<unknown>>(innerObservable: O, resultSelector: (outerValue: T, innerValue: ObservedValueOf<O>, outerIndex: number, innerIndex: number) => R, concurrent?: number): OperatorFunction<T, R>;
//# sourceMappingURL=mergeMapTo.d.ts.map