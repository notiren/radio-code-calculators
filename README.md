# Radio Code Calculators

Static, client-side web apps that recover car radio unlock codes. Everything runs
in the browser, no data is ever sent to a server.

Two calculators are included:

- **Ford** — looks up the code from the radio serial (M or V + 6 digits) using a
  4 MB binary table (`fordradiocodes.bin`).
- **Renault** — generates the code from the pre-code (a letter + 3 digits) with a
  pure algorithm (no data file needed).

## Ford: how it works

Unlike Renault, Ford codes have no simple formula, the serial-to-code mapping is
effectively a keyed table, so the full lookup table must be shipped. It comes from
the [DavidB445/fz_fordradiocodes](https://github.com/DavidB445/fz_fordradiocodes)
Flipper Zero plugin.

`fordradiocodes.bin` (4 MB, 2,000,000 codes) stores each code as a little-endian
`uint16`:

- **M-series:** byte offset `index * 2`
- **V-series:** byte offset `2,000,000 + index * 2`

The page fetches the `.bin` once, then does an O(1) offset read per lookup.

## Renault: how it works

The code is derived arithmetically from the pre-code (ported from the
[radcoderen](https://github.com/radcoderen/radcoderen.github.io) project). Pre-codes
starting with `A0` are not supported by the algorithm.

## Live site (GitHub Pages)

The published site lives in `docs/`:

```
docs/
├─ index.html                 landing page — choose Ford or Renault
├─ .nojekyll                  serve files as-is (don't run Jekyll)
├─ ford/
│  ├─ index.html              Ford calculator
│  └─ fordradiocodes.bin      code database
└─ renault/
   └─ index.html              Renault calculator
```

To enable: **Settings → Pages → Source: Deploy from a branch**, branch `main`,
folder `/docs`. The site will be at
[https://notiren.github.io/radio-code-calculators/](https://notiren.github.io/radio-code-calculators/).

## Local development

```powershell
python -m http.server 8000 --directory docs
# then open http://localhost:8000
```

## Regenerating the Ford database

`extract-ford-code.py` contains the extraction logic and a
`dump_entire_bin_to_csv()` helper used to produce `extracted_codes.csv`
(not required by the website).

## Credits

- **Ford** code database: [DavidB445/fz_fordradiocodes](https://github.com/DavidB445/fz_fordradiocodes)
- **Renault** algorithm: [radcoderen](https://github.com/radcoderen/radcoderen.github.io)
