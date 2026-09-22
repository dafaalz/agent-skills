# Legal and Ethical Boundaries in Web Design Reverse Engineering

Legal doctrines, intellectual property boundaries, and clean-room operational protocols for reverse-engineering web interfaces.

## Core Legal Doctrines

Reverse engineering web designs requires clear separation between functional ideas, which remain uncopyrightable, and creative expression, which receives copyright and trade dress protection. Copying structural layouts, responsive grids, and standard user flows does not constitute copyright infringement. In contrast, copying graphic artwork, original copy, proprietary source code, or trademark brand identities triggers civil liability.

The following eight legal precedents and industry authorities govern web reverse engineering:

### 1. Computer Associates International, Inc. v. Altai, Inc., 982 F.2d 693 (2d Cir. 1992)
Official source: https://law.justia.com/cases/federal/appellate-courts/F2/982/693/

This decision established the Abstraction-Filtration-Comparison Test (AFC Test) to evaluate software architecture and code similarity. The court divides a work into abstraction layers, then filters out non-protectable elements under 17 U.S.C. § 102(b). Filtered elements include pure ideas, implementations dictated by technical efficiency (merger doctrine), and industry conventions (scènes à faire).

In web engineering, standard CSS grid scaffolding, responsive viewport breakpoints, flexbox alignment rows, and ubiquitous navigation schemes filter out as public domain components. Protected elements remain strictly limited to narrative text, custom SVG illustrations, photography, proprietary icon sets, and non-functional creative styling expressions.

### 2. Apple Computer, Inc. v. Microsoft Corp., 35 F.3d 1435 (9th Cir. 1994)
Official source: https://law.justia.com/cases/federal/appellate-courts/F3/35/1435/

This ruling limited copyright protection for Graphical User Interfaces (GUIs) and rejected monopoly claims over look and feel. Standard interface metaphors, including overlapping windows, folder icons, top-level menu bars, and dropdown menus, were ruled scènes à faire.

Because graphical interfaces consist primarily of common conventions, user interfaces receive only thin copyright. A plaintiff must demonstrate virtual identity (pixel-for-pixel cloning), rather than general substantial similarity. Engineers remain free to adopt modern patterns like floating navbars, bento grids, and collapsible sidebars, provided they author visual assets and micro-styling independently.

### 3. Lotus Development Corp. v. Borland International, Inc., 516 U.S. 233 (1996)
Official source: https://supreme.justia.com/cases/federal/us/516/233/

The United States Supreme Court affirmed that a method of operation is excluded from copyright protection under 17 U.S.C. § 102(b). Command menu hierarchies and operational action sequences constitute functional methods rather than artistic expressions.

In web applications, multi-step onboarding flows, checkout form sequences, e-commerce filter taxonomies, and keyboard shortcuts constitute methods of operation. Replicating these flows remains legal to preserve user ergonomics and learned mental models. However, explanatory tooltips, instructional text, and original microcopy inside those flows remain protected by literary copyright.

### 4. Google LLC v. Oracle America, Inc., 593 U.S. 1 (2021)
Official source: https://supreme.justia.com/cases/federal/us/593/18-956/

The Supreme Court applied the Fair Use doctrine to declaring code and software interfaces. Copying declarative interfaces to allow developers to bring their knowledge to new platforms serves a transformative purpose.

In web component architecture, aligning component prop signatures, Tailwind theme token schemas, and public API interfaces is permissible to ensure developer ergonomics. However, implementing code behind those interfaces must be written independently without copying vendor internal implementations.

### 5. Compendium of U.S. Copyright Office Practices, Third Edition (2021)
Official source: https://www.copyright.gov/comp3/chap1000/ch1000-websites.pdf

Chapter 1000 (§ 1007.4) and Chapter 300 (§ 313.4(J)) state that layout, visual formatting, and general website look and feel are ineligible for copyright registration. Copyright coverage extends only to original separable content, specifically narrative text, photographic images, graphic illustrations, video files, and human-written source code.

Engineers are permitted to deconstruct and adopt wireframe layouts, such as 50/50 hero splits, three-column pricing tables, or sticky sidebar arrangements. Teams must populate those wireframes with original copywriting, licensed photography, and open-source typography.

### 6. Lanham Act § 43(a) and Trade Dress Doctrine
Official source: https://supreme.justia.com/cases/federal/us/505/763/

Under Two Pesos v. Taco Cabana (1992) and Blue Nile v. Ice.com (2007), trade dress protects the overall commercial image of a product if the appearance is non-functional, has acquired distinctiveness, and causes a likelihood of consumer confusion regarding business origin.

Engineers must avoid creating knockoff sites that mirror trademark branding, including logos, deceptive domain names, mascots, distinctive brand color pairings, and proprietary art direction. Passing off or brand spoofing triggers trademark infringement and unfair competition claims without requiring proof of copied code.

### 7. Electronic Frontier Foundation (EFF) Coders Rights Project
Official source: https://www.eff.org/issues/coders/reverse-engineering-faq

The EFF confirms that reverse engineering for system analysis and interoperability constitutes fair use. However, this defense fails if extraction circumvents digital protection systems under DMCA § 1201 or breaches binding Terms of Service on authenticated, paywalled web applications. Extraction must remain restricted to public, unauthenticated web pages without bypassing technical locks.

### 8. Austin Kleon, Steal Like an Artist (2012)
Official source: https://austinkleon.com/steal/

Kleon defines the ethical boundary between good theft and bad theft. Ethical adaptation honors the original work, deconstructs underlying principles, combines multiple influences, and produces transformative output. Bad theft copies a single source directly without understanding the underlying mechanics, which damages professional standing and invites legal action.

---

## Legal Boundary Matrix

| Interface Element | Legal Status | Permitted Action | Prohibited Action |
|---|---|---|---|
| Macro Layout | Permitted | Replicate CSS grid tracks, bento structures, or flexbox rows | Copy raw minified HTML documents from vendor origins |
| Navigation Flow | Permitted | Adopt step sequences, wizard flows, and filter trees | Copy instructional microcopy and marketing text |
| Design Tokens | Permitted | Extract modular scale ratios, spacing multipliers, and radii | Copy proprietary internal token naming schemes |
| Copy Content | Prohibited | Write original marketing text or use clean placeholder copy | Scrape and reuse production landing page articles |
| Graphic Media | Prohibited | Generate clean icons or license independent photography | Download proprietary SVG illustrations and client photos |
| Brand Identity | Prohibited | Create unique logos, brand names, and distinct color schemes | Reproduce brand assets that create trade dress confusion |
| Component Props | Permitted | Standardize declarative component props for ergonomic consistency | Copy private hook state logic and minified bundle internals |

---

## Clean-Room Operational Protocol

Maintain structural isolation during commercial reverse engineering by assigning roles across a Chinese wall:

1. **Analyst (Dirty Room).** Inspects the target website in developer tools, measures bounding box geometry, extracts computed typography scales, records animation cubic-bezier coordinates, and catalogs color tokens. The analyst writes an abstract design specification without copying proprietary code or copyrighted media assets.
2. **Compliance Reviewer.** Inspects the draft specification to ensure no copyrighted text, brand trade dress, or vendor code snippets persist in the document.
3. **Builder (Clean Room).** Receives the approved specification document. The builder writes clean components, modern stylesheets, and interaction handlers from scratch without directly inspecting the target origin.
