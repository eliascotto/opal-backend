import { operate } from '../util/lift';
import { concatAll } from './concatAll';
import { internalFromArray } from '../observable/fromArray';
import { popScheduler } from '../util/args';
export function concatWith(...otherSources) {
    return concat(...otherSources);
}
export function concat(...args) {
    const scheduler = popScheduler(args);
    return operate((source, subscriber) => {
        concatAll()(internalFromArray([source, ...args], scheduler)).subscribe(subscriber);
    });
}
//# sourceMappingURL=concatWith.js.map