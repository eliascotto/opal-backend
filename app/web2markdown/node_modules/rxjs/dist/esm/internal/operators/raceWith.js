import { raceInit } from '../observable/race';
import { operate } from '../util/lift';
import { argsOrArgArray } from "../util/argsOrArgArray";
import { identity } from '../util/identity';
export function race(...args) {
    return raceWith(...argsOrArgArray(args));
}
export function raceWith(...otherSources) {
    return !otherSources.length ? identity : operate((source, subscriber) => {
        raceInit([source, ...otherSources])(subscriber);
    });
}
//# sourceMappingURL=raceWith.js.map