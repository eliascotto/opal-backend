import { combineLatest } from '../observable/combineLatest';
import { joinAllInternals } from './joinAllInternals';
export function combineAll(project) {
    return joinAllInternals(combineLatest, project);
}
//# sourceMappingURL=combineAll.js.map