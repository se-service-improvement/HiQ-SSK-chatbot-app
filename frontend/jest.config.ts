import type {Config} from '@jest/types';
// Sync object
const config: Config.InitialOptions = {
  verbose: true,
  transform: {
***REMOVED***'^.+\\.tsx?$': 'ts-jest',
  },
};
export default config;