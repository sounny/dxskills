/**
 * DxSkills Quiet Typo and Inversion Normalizer
 *
 * Normalizes common dyslexic letter inversions and phonetic slips quietly
 * without triggering red squiggly visual anxiety.
 */

const COMMON_INVERSIONS: Record<string, string> = {
  "teh": "the",
  "taht": "that",
  "waht": "what",
  "wierd": "weird",
  "recieved": "received",
  "recieve": "receive",
  "recieving": "receiving",
  "calender": "calendar",
  "definately": "definitely",
  "definitly": "definitely",
  "seperate": "separate",
  "seperation": "separation",
  "acheive": "achieve",
  "acheived": "achieved",
  "embarass": "embarrass",
  "embarassed": "embarrassed",
  "occurance": "occurrence",
  "untill": "until",
  "alot": "a lot",
  "wich": "which",
  "thier": "their",
  "freind": "friend",
  "freinds": "friends",
  "peice": "piece",
  "peices": "pieces",
  "beleive": "believe",
  "beleived": "believed",
  "goverment": "government",
  "enviroment": "environment",
  "tommorrow": "tomorrow",
  "neccessary": "necessary",
  "begining": "beginning",
  "truely": "truly"
};

function matchCase(source: string, target: string): string {
  if (source === source.toUpperCase()) {
    return target.toUpperCase();
  }
  if (source[0] === source[0].toUpperCase()) {
    return target.charAt(0).toUpperCase() + target.slice(1);
  }
  return target.toLowerCase();
}

export function quietNormalizeText(text: string): { normalized: string; changesCount: number } {
  let count = 0;
  const wordRegex = /\b[a-zA-Z]+\b/g;

  const normalized = text.replace(wordRegex, (matched) => {
    const lower = matched.toLowerCase();
    if (Object.prototype.hasOwnProperty.call(COMMON_INVERSIONS, lower)) {
      count++;
      return matchCase(matched, COMMON_INVERSIONS[lower]);
    }
    return matched;
  });

  return { normalized, changesCount: count };
}
