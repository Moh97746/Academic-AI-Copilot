"""
SciWrite Reviewer - Automated Academic Writing Quality Audit
Based on Dr. Kristin Sainani's 'Writing in the Sciences' methodology.

This module provides a 5-pass review pipeline that systematically
improves academic manuscript quality before journal submission.
"""

import re
import json
from collections import Counter


class SciWriteReviewer:
    """
    Multi-stage academic text reviewer implementing five audit passes:
    1. Clutter Extraction - Remove unnecessary words and redundancy
    2. Voice & Verb Vitality - Prefer active voice and strong verbs
    3. Sentence Architecture - Ensure proper structure and flow
    4. Keyword Consistency - Verify terminology uniformity
    5. Numerical & Citation Integrity - Validate references and data
    """

    # Common academic clutter phrases to flag
    CLUTTER_PHRASES = [
        "it is well known that",
        "it should be noted that",
        "it is important to note that",
        "in order to",
        "due to the fact that",
        "a large number of",
        "a majority of",
        "as a matter of fact",
        "at the present time",
        "for the purpose of",
        "in the event that",
        "it has been shown that",
        "on the basis of",
        "with regard to",
        "in terms of",
        "the fact that",
        "it is worth noting that",
        "it is evident that",
        "it can be seen that",
        "there is no doubt that",
    ]

    # Weak verb patterns (passive voice indicators)
    PASSIVE_PATTERNS = [
        r"\bis\s+\w+ed\b",
        r"\bwas\s+\w+ed\b",
        r"\bwere\s+\w+ed\b",
        r"\bbeen\s+\w+ed\b",
        r"\bare\s+\w+ed\b",
    ]

    def __init__(self, text):
        self.original_text = text
        self.sentences = self._split_sentences(text)
        self.findings = {
            "pass_1_clutter": [],
            "pass_2_voice": [],
            "pass_3_structure": [],
            "pass_4_keywords": [],
            "pass_5_citations": [],
        }

    def _split_sentences(self, text):
        """Split text into sentences while preserving abbreviations."""
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [s.strip() for s in sentences if s.strip()]

    def pass_1_clutter_extraction(self):
        """Identify and flag clutter phrases in the text."""
        for phrase in self.CLUTTER_PHRASES:
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            matches = pattern.findall(self.original_text)
            if matches:
                self.findings["pass_1_clutter"].append({
                    "phrase": phrase,
                    "count": len(matches),
                    "suggestion": self._get_clutter_fix(phrase),
                })
        return self.findings["pass_1_clutter"]

    def pass_2_voice_vitality(self):
        """Detect passive voice constructions."""
        for i, sentence in enumerate(self.sentences):
            for pattern in self.PASSIVE_PATTERNS:
                if re.search(pattern, sentence, re.IGNORECASE):
                    self.findings["pass_2_voice"].append({
                        "sentence_index": i + 1,
                        "sentence": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                        "issue": "Passive voice detected",
                    })
                    break
        return self.findings["pass_2_voice"]

    def pass_3_sentence_architecture(self):
        """Check sentence length and complexity."""
        for i, sentence in enumerate(self.sentences):
            word_count = len(sentence.split())
            if word_count > 40:
                self.findings["pass_3_structure"].append({
                    "sentence_index": i + 1,
                    "word_count": word_count,
                    "issue": "Sentence too long (>40 words). Consider splitting.",
                    "preview": sentence[:80] + "...",
                })
            elif word_count < 5 and not sentence.endswith("?"):
                self.findings["pass_3_structure"].append({
                    "sentence_index": i + 1,
                    "word_count": word_count,
                    "issue": "Fragment detected. May need expansion.",
                    "preview": sentence,
                })
        return self.findings["pass_3_structure"]

    def pass_4_keyword_consistency(self):
        """Check for inconsistent terminology usage."""
        # Extract potential technical terms (capitalized multi-word phrases)
        terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', self.original_text)
        term_counts = Counter(terms)

        # Find abbreviations and check if they are defined
        abbreviations = re.findall(r'\b[A-Z]{2,6}\b', self.original_text)
        abbrev_counts = Counter(abbreviations)

        for abbrev, count in abbrev_counts.items():
            if count >= 2:
                # Check if abbreviation is defined (appears in parentheses after full form)
                definition_pattern = rf'\([^)]*{re.escape(abbrev)}[^)]*\)'
                if not re.search(definition_pattern, self.original_text):
                    self.findings["pass_4_keywords"].append({
                        "abbreviation": abbrev,
                        "count": count,
                        "issue": f"Abbreviation '{abbrev}' used {count} times but may not be formally defined.",
                    })
        return self.findings["pass_4_keywords"]

    def pass_5_citation_integrity(self):
        """Validate citation format consistency and count."""
        # Check for numbered citations [1], [2], etc.
        numbered_refs = re.findall(r'\[(\d+)\]', self.original_text)
        # Check for author-year citations (Author, Year)
        author_year_refs = re.findall(r'\([A-Z][a-z]+(?:\s+et\s+al\.?)?,\s*\d{4}\)', self.original_text)

        if numbered_refs and author_year_refs:
            self.findings["pass_5_citations"].append({
                "issue": "Mixed citation styles detected (numbered + author-year). Standardize to one format.",
                "numbered_count": len(numbered_refs),
                "author_year_count": len(author_year_refs),
            })

        if numbered_refs:
            ref_numbers = sorted(set(int(r) for r in numbered_refs))
            expected = list(range(1, max(ref_numbers) + 1))
            missing = set(expected) - set(ref_numbers)
            if missing:
                self.findings["pass_5_citations"].append({
                    "issue": f"Missing in-text citations for references: {sorted(missing)}",
                })

        return self.findings["pass_5_citations"]

    def run_full_review(self):
        """Execute all 5 review passes and return comprehensive report."""
        self.pass_1_clutter_extraction()
        self.pass_2_voice_vitality()
        self.pass_3_sentence_architecture()
        self.pass_4_keyword_consistency()
        self.pass_5_citation_integrity()

        total_issues = sum(len(v) for v in self.findings.values())

        report = {
            "summary": {
                "total_sentences": len(self.sentences),
                "total_words": len(self.original_text.split()),
                "total_issues_found": total_issues,
                "quality_score": max(0, 100 - (total_issues * 3)),
            },
            "detailed_findings": self.findings,
        }
        return report

    def _get_clutter_fix(self, phrase):
        """Provide a concise replacement for common clutter phrases."""
        fixes = {
            "in order to": "to",
            "due to the fact that": "because",
            "a large number of": "many",
            "a majority of": "most",
            "as a matter of fact": "(delete)",
            "at the present time": "now / currently",
            "for the purpose of": "to / for",
            "in the event that": "if",
            "on the basis of": "based on",
            "with regard to": "regarding / about",
            "in terms of": "in / for",
            "the fact that": "(rephrase)",
        }
        return fixes.get(phrase.lower(), "Consider removing or simplifying.")

    def print_report(self):
        """Print a human-readable review report."""
        report = self.run_full_review()
        print("=" * 60)
        print("  SciWrite Academic Review Report")
        print("=" * 60)
        print(f"  Total Sentences : {report['summary']['total_sentences']}")
        print(f"  Total Words     : {report['summary']['total_words']}")
        print(f"  Issues Found    : {report['summary']['total_issues_found']}")
        print(f"  Quality Score   : {report['summary']['quality_score']}/100")
        print("=" * 60)

        for pass_name, issues in report["detailed_findings"].items():
            if issues:
                print(f"\n  [{pass_name.upper()}]")
                for issue in issues:
                    for k, v in issue.items():
                        print(f"    {k}: {v}")
                    print()


if __name__ == "__main__":
    sample = """
    It is well known that solar irradiance forecasting is important for microgrids.
    In order to improve accuracy, a novel physics-informed model was proposed by the authors.
    The model was trained on data that was collected from NASA POWER API.
    Due to the fact that traditional models fail under cloud transients, our approach
    uses thermodynamic constraints. A large number of experiments were conducted.
    The CNN-BiLSTM architecture is combined with Cross-Attention (CA) mechanisms [1].
    Results show improvement over baseline methods [3] and recent work [5].
    """
    reviewer = SciWriteReviewer(sample)
    reviewer.print_report()
