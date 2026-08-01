# Domain 6 (health capacity) — decision

**Decided 2026-08-01, before any data contact. No series was fetched or
inspected before this was written.**

Options and tradeoffs: [`domain-6-options.md`](domain-6-options.md).

---

## The decision

**Ship both series. OECD hospital beds per 1,000 is the primary. BLS registered
nurses per capita is a Study 1 descriptive companion only.**

Naming the primary now is the point of writing this before the fetch. It cannot
be swapped later for whichever series turns out to say the more interesting
thing.

| | Series | Role |
|---|---|---|
| **Primary** | OECD hospital beds per 1,000, US | Domain 6 in Study 1 **and** Study 2 |
| **Companion** | BLS registered nurses per capita | Study 1 descriptive only. **Never enters Study 2.** |

## Why beds is primary — coverage, not preference

The preferred series on the merits was nurses per capita. Beds count physical
plant; what actually binds in a capacity crisis is staff. A bed without a nurse
absorbs nothing, and in 2020–21 US hospitals repeatedly had beds they could not
staff.

It is not primary anyway, and the reason is arithmetic rather than judgement.

Study 2 compares episodes before the era split against episodes after it. A
domain with no early-era episodes cannot support that comparison at all — the
frozen specification says so in §6 and scores such a domain "insufficient". BLS
OES coverage is believed to begin around 1997–99. If that is right, the series
has no pre-2000 episodes, and it cannot serve Study 2 no matter how well it
measures the construct.

So the choice is between a series that measures the right thing and cannot be
used, and a series that measures a proxy and can. For Study 2 there is no
choice.

*(The ~1997–99 start is from prior knowledge and is unverified — nothing was
fetched. If verification at gate-open shows coverage reaching back before 2000
with enough history for early-era episodes, that is a material change and gets
recorded as such. It does not silently promote the companion to primary; that
would require a dated, written amendment.)*

## Why the companion ships anyway

Beds and nurses carry confounds that point in **opposite** directions:

- **Beds drift down** for reasons unrelated to depletion — the deliberate shift
  to outpatient care. Spec v0.2 already discloses this.
- **Nurses drift up** for reasons unrelated to buffer strength — hiring tracks
  demand, so the series can rise exactly when a buffer measure should show
  strain.

Where they agree, the agreement means something. Where they diverge, the
divergence points at which confound is doing the work. A single series hides
that; two show it.

## Rules that bind this decision

1. **Study 2 uses beds. Only beds.** The nurses series never enters the ratchet
   analysis, in any form, whatever it shows.
2. **Both appear in Study 1**, each with its confound stated on the panel.
3. **The AHA substitution is a licence decision, not a data one.** AHA Hospital
   Statistics is Tier 3 under [`../DATA_TERMS.md`](../DATA_TERMS.md) — transcribed
   values with citation only — so it cannot anchor a pipeline anyone else can
   reproduce. It was set aside for that reason, before any of its numbers were
   seen.
4. **NCHS is not a workaround.** Where its figures reproduce AHA's, the tier
   follows the numbers.
5. **CMS was rejected** on the spec's own rule: building a national series from
   provider-level files is researcher re-derivation, which §3.0 criterion K2
   bars and which the domain-2 precedent ("published values only") already
   forbids.

## What a reader should take from this

Domain 6 measures physical hospital capacity. It does not measure staffed
capacity, which is the constraint more likely to bind in a real crisis. That
gap is a known weakness of the domain, disclosed here rather than discovered
later, and it is the reason the nurses series is carried alongside even though
it cannot bear any verdict.
