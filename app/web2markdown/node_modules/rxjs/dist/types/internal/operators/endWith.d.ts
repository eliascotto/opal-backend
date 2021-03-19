import { MonoTypeOperatorFunction, SchedulerLike, OperatorFunction, ValueFromArray } from '../types';
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function endWith<T>(scheduler: SchedulerLike): MonoTypeOperatorFunction<T>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function endWith<T, A>(v1: A, scheduler: SchedulerLike): OperatorFunction<T, T | A>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function endWith<T, A, B>(v1: A, v2: B, scheduler: SchedulerLike): OperatorFunction<T, T | A | B>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function endWith<T, A, B, C>(v1: A, v2: B, v3: C, scheduler: SchedulerLike): OperatorFunction<T, T | A | B | C>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function endWith<T, A, B, C, D>(v1: A, v2: B, v3: C, v4: D, scheduler: SchedulerLike): OperatorFunction<T, T | A | B | C | D>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function endWith<T, A, B, C, D, E>(v1: A, v2: B, v3: C, v4: D, v5: E, scheduler: SchedulerLike): OperatorFunction<T, T | A | B | C | D | E>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function endWith<T, A, B, C, D, E, F>(v1: A, v2: B, v3: C, v4: D, v5: E, v6: F, scheduler: SchedulerLike): OperatorFunction<T, T | A | B | C | D | E | F>;
export declare function endWith<T, A extends any[] = T[]>(...args: A): OperatorFunction<T, T | ValueFromArray<A>>;
//# sourceMappingURL=endWith.d.ts.map