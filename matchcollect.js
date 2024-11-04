const fetch = require('node-fetch');
const ObjectsToCsv = require('objects-to-csv');
const fs = require('fs');

const API_TOKEN = 'e368ea2f30cb4af38de0b027d56bdd6b'; // Use the token from environment variables
const BASE_URL = 'https://api.football-data.org/v4';
const LEAGUE_ID = 'PL'; // EPL league code

// Fetch data from Football-Data.org API
async function fetchData(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: { 'X-Auth-Token': API_TOKEN },
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }
  return response.json();
}

// Fetch EPL results (Completed Matches)
async function fetchResults() {
  const data = await fetchData(`/competitions/${LEAGUE_ID}/matches?status=FINISHED`);
  return data.matches.map(match => ({
    date: match.utcDate,
    homeTeam: match.homeTeam.name,
    awayTeam: match.awayTeam.name,
    homeScore: match.score.fullTime.home,
    awayScore: match.score.fullTime.away,
  }));
}

// Fetch upcoming EPL fixtures (Scheduled Matches)
async function fetchFixtures() {
  const data = await fetchData(`/competitions/${LEAGUE_ID}/matches?status=SCHEDULED`);
  return data.matches.map(match => ({
    date: match.utcDate,
    homeTeam: match.homeTeam.name,
    awayTeam: match.awayTeam.name,
  }));
}

// Save data to CSV
async function saveToCsv(data, filename) {
  const csv = new ObjectsToCsv(data);
  await csv.toDisk(`./${filename}`);
  console.log(`${filename} saved successfully!`);
}

// Main function to fetch and save data
async function main() {
  try {
    console.log('Fetching EPL results...');
    const results = await fetchResults();
    await saveToCsv(results, 'epl_results.csv');

    console.log('Fetching upcoming EPL fixtures...');
    const fixtures = await fetchFixtures();
    await saveToCsv(fixtures, 'epl_fixtures.csv');

    console.log('Data fetched and saved successfully.');
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

main();
