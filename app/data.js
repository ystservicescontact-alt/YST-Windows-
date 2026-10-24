// Reference data: job categories, default job lengths, GTA towns, sample day.

const CATEGORIES = [
  { id: 'window', label: 'Windows' },
  { id: 'sliding', label: 'Sliding doors' },
  { id: 'garage', label: 'Garage doors' },
  { id: 'door', label: 'Entry doors' },
  { id: 'other', label: 'Other' },
];

const WORK = [
  { id: 'repair', label: 'Repair' },
  { id: 'install', label: 'Install' },
  { id: 'estimate', label: 'Estimate' },
];

// Minutes on site, by work type then category.
const DEFAULT_DURATIONS = {
  repair:   { window: 60,  sliding: 75,  garage: 90,  door: 60,  other: 60 },
  install:  { window: 150, sliding: 180, garage: 240, door: 180, other: 120 },
  estimate: { window: 30,  sliding: 30,  garage: 30,  door: 30,  other: 30 },
};

// Route colours. Each one reads on both light and dark backgrounds.
const PALETTE = ['#2F6FDE', '#E0612B', '#169B62', '#9B4DCA', '#C9930A', '#D23C6E', '#1494B8', '#7A8B2E'];

// Town centres, used to name areas and to place an address when exact lookup isn't available.
// [name, lat, lng, showOnMap]
const CITIES = [
  ['Toronto', 43.6532, -79.3832, 1], ['North York', 43.7615, -79.4111, 1], ['Scarborough', 43.7764, -79.2318, 1],
  ['Etobicoke', 43.6205, -79.5132, 1], ['East York', 43.6910, -79.3280, 0], ['York', 43.6896, -79.4874, 0],
  ['Mississauga', 43.5890, -79.6441, 1], ['Port Credit', 43.5510, -79.5860, 0], ['Streetsville', 43.5860, -79.7140, 0],
  ['Brampton', 43.7315, -79.7624, 1], ['Bolton', 43.8758, -79.7339, 0], ['Caledon', 43.8668, -79.8580, 0],
  ['Vaughan', 43.8361, -79.4983, 1], ['Woodbridge', 43.7840, -79.5960, 0], ['Maple', 43.8500, -79.5100, 0],
  ['Concord', 43.8000, -79.4800, 0], ['Kleinburg', 43.8380, -79.6280, 0], ['Thornhill', 43.8150, -79.4240, 0],
  ['Richmond Hill', 43.8828, -79.4403, 1], ['Markham', 43.8561, -79.3370, 1], ['Unionville', 43.8680, -79.3110, 0],
  ['Stouffville', 43.9710, -79.2440, 1], ['King City', 43.9290, -79.5280, 0], ['Aurora', 44.0065, -79.4504, 1],
  ['Newmarket', 44.0592, -79.4613, 1], ['Bradford', 44.1145, -79.5630, 1], ['Keswick', 44.2500, -79.4667, 0],
  ['Oakville', 43.4675, -79.6877, 1], ['Burlington', 43.3255, -79.7990, 1], ['Milton', 43.5183, -79.8774, 1],
  ['Georgetown', 43.6500, -79.9170, 0], ['Hamilton', 43.2557, -79.8711, 1], ['Pickering', 43.8384, -79.0868, 1],
  ['Ajax', 43.8509, -79.0204, 1], ['Whitby', 43.8975, -78.9429, 1], ['Oshawa', 43.8971, -78.8658, 1],
  ['Uxbridge', 44.1090, -79.1210, 0],
];

function findCity(text) {
  if (!text) return null;
  const t = String(text).toLowerCase();
  // Longest names first so "North York" wins over "York".
  const sorted = [...CITIES].sort((a, b) => b[0].length - a[0].length);
  return sorted.find(c => t.includes(c[0].toLowerCase())) || null;
}

function nearestCity(lat, lng) {
  let best = null, bestD = Infinity;
  for (const c of CITIES) {
    const d = (c[1] - lat) ** 2 + ((c[2] - lng) * 0.72) ** 2;
    if (d < bestD) { bestD = d; best = c; }
  }
  return best ? best[0] : '';
}

// Guess category and work type from a Workiz job type or free text.
function classifyJob(text) {
  const t = String(text || '').toLowerCase();
  let category = 'window', guessed = true;
  if (/garage|overhead|opener|torsion|spring/.test(t)) { category = 'garage'; guessed = false; }
  else if (/slid|patio|balcony|terrace/.test(t)) { category = 'sliding'; guessed = false; }
  else if (/door|lock|hinge|entry|weatherstrip/.test(t)) { category = 'door'; guessed = false; }
  else if (/window|glass|seal|fog|igu|pane|crank|casement|awning|screen|thermal|sash|tilt/.test(t)) { category = 'window'; guessed = false; }
  let work = 'repair';
  if (/install|replace|replacement|new unit|new door|new window/.test(t)) work = 'install';
  else if (/estimate|quote|consult|measure|inspection|assessment/.test(t)) work = 'estimate';
  return { category, work, guessed: guessed && !!t.trim() };
}

function sampleData(date) {
  const techs = [
    { id: 't1', name: 'Eli', color: PALETTE[0], start: '08:00', end: '17:00', maxJobs: 6, active: true,
      home: { address: 'Rutherford Rd', city: 'Vaughan', lat: 43.8361, lng: -79.4983 },
      skills: ['window:repair', 'window:install', 'garage:repair', 'garage:install', 'sliding:repair', 'sliding:install'] },
    { id: 't2', name: 'Ron', color: PALETTE[1], start: '08:00', end: '17:00', maxJobs: 6, active: true,
      home: { address: 'Hurontario St', city: 'Mississauga', lat: 43.5890, lng: -79.6441 },
      skills: ['window:repair'] },
    { id: 't3', name: 'Sam', color: PALETTE[2], start: '08:30', end: '17:30', maxJobs: 6, active: true,
      home: { address: 'Ellesmere Rd', city: 'Scarborough', lat: 43.7764, lng: -79.2318 },
      skills: ['window:repair', 'sliding:repair', 'door:repair'] },
  ];
  const j = (n, client, type, address, city, lat, lng, ws, we, notes) => {
    const c = classifyJob(type);
    return { id: 's' + n, source: 'sample', ref: 'S-' + (1040 + n), date, client, phone: '(416) 555-01' + String(10 + n),
      type, category: c.category, work: c.work, duration: DEFAULT_DURATIONS[c.work][c.category],
      address, city, lat, lng, precise: true, windowStart: ws || '', windowEnd: we || '', notes: notes || '', lockTech: '' };
  };
  const jobs = [
    j(1, 'Patel', 'Foggy window glass repair', '3050 Confederation Pkwy', 'Mississauga', 43.5935, -79.6466, '09:00', '12:00'),
    j(2, 'Nguyen', 'Garage door spring repair', '25 Peel Centre Dr', 'Brampton', 43.7174, -79.7230),
    j(3, 'Romano', 'Window balancer repair', '5 Islington Ave', 'Etobicoke', 43.6236, -79.5161),
    j(4, 'Walsh', 'Window crank repair', '1200 Lakeshore Rd E', 'Oakville', 43.4572, -79.6646, '', '', 'Two casement cranks, kitchen and bedroom'),
    j(5, 'Cohen', 'Garage door install', '9350 Yonge St', 'Richmond Hill', 43.8742, -79.4405, '08:00', '11:00', 'Single 9x7 insulated door'),
    j(6, 'Silva', 'Casement window replacement install', '2900 Major Mackenzie Dr', 'Vaughan', 43.8530, -79.5280),
    j(7, 'Brown', 'Window seal repair', '1900 Ellesmere Rd', 'Scarborough', 43.7790, -79.2240),
    j(8, 'Kim', 'Entry door lock and hinge repair', '5000 Hwy 7', 'Markham', 43.8640, -79.3020, '13:00', '16:00'),
    j(9, 'Haddad', 'Sliding patio door roller repair', '4800 Yonge St', 'North York', 43.7615, -79.4111),
    j(10, 'Martin', 'Window repair', '1355 Kingston Rd', 'Pickering', 43.8320, -79.0880, '12:00', '17:00'),
  ];
  return { techs, jobs };
}
