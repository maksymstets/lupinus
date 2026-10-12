# Health-Intelligence_Conference_2026_Stets_Havryliak
This repo contains scripts for bulk BIOPEP digestion simulation, ADMET analysis via ADMET-AI and molecular docking via AutoDockVina.

The results were reported at Health Intelligence Conference 2026 in August, 2026 (Kyiv, Ukraine). 

The research workflow was adopted from Arámburo-Gálvez et al., 2024 (https://doi.org/10.3390/ijms252312866), with modifications.
The aim of this work on predicting ACE and DPP-IV inhibitory peptides from *Lupinus albus*, using a combination of in silico hydrolysis, molecular docking, and ADMET profiling.

Clinical motivation is straightforward. ACE, angiotensin-converting enzyme, is a central target in hypertension management, and DPP-IV, dipeptidyl peptidase IV, is a central target in type 2 diabetes management. Both are currently addressed with synthetic pharmaceuticals, but there’s a growing body of research looking for food-derived, natural peptide alternatives, ideally ones that could come from an already-consumed, protein-rich crop. That’s the space our work sits in.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx" src="https://github.com/user-attachments/assets/518505e0-c5e0-4855-9efb-ecafb76c5351" />

## Lupin as an underutilized protein source
So, why lupin, and specifically, why Lupinus albus?

Lupin seeds are a genuinely underexploited source of functional protein. Hulled seeds reach 40 to 50 percent protein content, with 9 to 12 percent lipid and around 40 percent carbohydrate — protein levels in the same range as soy, but without soy’s level of research attention or market saturation.

Current applications are fairly conventional: animal feed, bakery, pasta, dairy alternatives. Emerging applications include meat alternatives, nutraceuticals, sports nutrition, and functional desserts. And on the horizon, there’s real potential in biofilms, nanotechnology, biotechnology, and circular-economy applications.

Now, here’s a point I want to emphasize specifically: most of the existing bioactive peptide literature on lupin, including the reference methodology paper we based our pipeline on, focuses on *Lupinus angustifolius*, narrow-leafed lupin. It’s the more commercially cultivated and more extensively characterized species. *Lupinus albus*, white lupin, by comparison, is considerably less studied from a bioactive peptide perspective, despite having a comparable or even higher protein content and a long history of cultivation, particularly in Mediterranean regions. This creates a genuine knowledge gap. If *L. albus* conglutins turn out to be just as rich a source of ACE-I and DPP-IV inhibitory peptides as *L. angustifolius*, that substantially broadens the pool of lupin species worth pursuing industrially and pharmacologically — rather than concentrating all research and breeding effort on a single species. That species choice is one of the key ways our study differs from, and extends, the reference paper.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx (1)" src="https://github.com/user-attachments/assets/808b3a82-37ef-40d7-a921-cdf603c1fd4f" />

## Workflow
We began with lupin conglutin, which constitutes roughly 95 percent of total lupin seed protein, with sequences retrieved from the UniProtKB database. From there we moved into in silico enzymatic and gastrointestinal hydrolysis, simulated through the BIOPEP-UWM platform.

We simulated digestion using eight enzymes, drawn from the enzyme panel used in the methodology study we followed: chymotrypsin, ficin, papain, pepsin at two different pH conditions, stem bromelain, subtilisin, and trypsin, plus a combined simulated gastrointestinal digestion condition that models the sequential action of pepsin followed by pancreatic enzymes, approximating what would happen as the protein passes through the stomach and small intestine. Each of these enzymes cleaves the conglutin sequence at different, enzyme-specific cleavage sites, so each one releases a distinct, sometimes overlapping set of peptide fragments. Running all eight in parallel, rather than relying on a single enzyme, gives us a much broader and more realistic picture of what peptides could plausibly be released, whether through digestion or through industrial enzymatic processing.

From that released peptide pool, we ran two parallel computational analyses. Molecular docking, using AutoDock Vina, to predict binding affinity to the ACE and DPP-IV target enzymes. It worth to note that no visualisation of best docking was performed at a time of a presentation. And ADMET prediction, using ADMET-AI, to evaluate pharmacokinetic and safety properties. Original paper tool - web-based ADMETLab 2.0, was purely suited for bulk analysis of large datasets and did not provide an API. That is why we used ADMET-AI, which is CLI tool nice run locally.

I want to stress why we didn’t stop at docking alone. A peptide can look like an excellent binder on paper and still be completely useless as a therapeutic or nutraceutical candidate if it’s poorly absorbed or toxic. So from the outset, our selection criteria were explicitly twofold: we were looking for peptides that are simultaneously strong binders and non-toxic and bioavailable. That dual filter, efficacy plus safety and absorbability, is what shapes every downstream result I’ll show you.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx (2)" src="https://github.com/user-attachments/assets/2d3857a5-38a1-4454-9a04-79d6a720735c" />

## Conglutins are rich in inhibitory peptides

Running this full pipeline, we identified 4,184 distinct peptides from lupin conglutin. Of these, 1,092 were predicted as ACE-I inhibitors and 1,313 as DPP-IV inhibitors, with the remaining roughly 1,779 peptides distributed across 58 other bioactivity types, osteoprotective, anti-inflammatory, antioxidant, anti-amnesic, anticancer, antibacterial, and more.

Now, an important caveat I want to flag clearly here: these 4,184 peptides are hypothetically possible peptides derived purely from the protein sequence. This number reflects everything that could theoretically be cleaved out of the conglutin sequence under the various enzymatic conditions we simulated, it is not a measurement of what has actually been isolated, detected, or confirmed to exist in real hydrolysates. It’s a computational upper bound, a map of possibility space, not a laboratory inventory. That distinction matters a lot for how we interpret every subsequent number in this talk, we’re working with predicted candidates, not confirmed compounds.

That said, even as a theoretical map, this result tells us something valuable: lupin conglutin is a genuinely dense reservoir of multifunctional bioactive sequences, with ACE and DPP-IV inhibition representing just two of many biologically relevant activities encoded within it.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx (3)" src="https://github.com/user-attachments/assets/bbcb7ae0-f188-4308-a341-306d8b9cf008" />

## Enzyme comparison
Next, we looked at which specific enzymes were most productive at generating ACE-I and DPP-IV inhibitory peptides, broken down across the different conglutin subunits — beta, delta, gamma, and legumin-type conglutins.

The pattern was consistent: pepsin, particularly under the low pH 1.3 condition, and papain generated the highest numbers of both ACE-I and DPP-IV inhibitory peptides across nearly all conglutin subunits. Trypsin was consistently the weakest performer by a wide margin. Practically speaking, this suggests that if someone wanted to actually produce these peptides at scale — whether through simulated gastric conditions or through industrial enzymatic hydrolysis — pepsin and papain would be the enzymes of choice.

But I do want to add an important limitation here, because it affects how far we can extrapolate these enzyme comparisons toward real-world practicality. All eight enzymes we modeled are well-characterized, specific proteases with known, discrete cleavage rules, that’s precisely what makes them tractable to simulate computationally. What we did not, and could not, easily model are non-specific proteases and complex protease mixtures, of the kind found in real digestive systems, in microbial fermentation, or in many industrial hydrolysis processes. Non-specific proteases don’t have a small number of well-defined cleavage rules; they cleave much more broadly and their activity is harder to characterize and encode in a platform like BIOPEP-UWM. Because of this, our enzyme comparison should be read as informative about relative trends among well-characterized, specific enzymes, not as a complete or fully practical picture of what would happen under real, more chaotic proteolytic conditions. This is a genuine limitation of the in silico approach.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx (4)" src="https://github.com/user-attachments/assets/1cb21330-d453-4915-b598-dcacdb28178c" />

## ADMET filtering

Moving to ADMET filtering — this is where our earlier point about looking for both strong binders and safe, bioavailable peptides really comes into play.

We took our pool of 205 unique bioactive peptides: 50 with ACE-I-only activity, 86 with DPP-IV-only activity, and 69 with dual activity against both targets. We then applied our ADMET criteria — a bioavailability score above 0.7, using ADMET-AI’s Bioavailability_Ma metric, and a toxicity score below 0.3 on the ClinTox scale.

After filtering, 71 peptides passed — a bit over a third of the starting pool. What I find particularly encouraging is that the dual-activity peptides held up disproportionately well: 34 of the original 69 dual-activity peptides passed both filters, meaning nearly half of them were both non-toxic and bioavailable, compared with roughly a fifth to a third for the single-activity groups. A peptide that simultaneously inhibits both ACE and DPP-IV, while also being predicted as safe and absorbable, is a particularly attractive candidate — potentially useful for managing hypertension and type 2 diabetes together, which is clinically relevant given how often these conditions co-occur.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx (5)" src="https://github.com/user-attachments/assets/d5de5f32-a5f0-4d1d-a750-7b869b52c4bd" />

## Docking affinities

Now let’s look at binding strength specifically. Our docking results showed affinities ranging from minus 9.1 to minus 5.3 kcal/mol for ACE-I candidates, and minus 8.2 to minus 5.5 kcal/mol for DPP-IV candidates — remember, more negative indicates stronger predicted binding.

For context: Lisinopril, a clinically used ACE inhibitor, binds at around minus 8.6 kcal/mol. Saxagliptin and Vildagliptin, both DPP-IV inhibitors in clinical use, bind at minus 8.4 and minus 8.8 kcal/mol respectively. Several of our top lupin-derived peptide candidates fall within, or even exceed, that same range — which is a strong indication that these are not just computational noise, but genuinely competitive binders at the *in silico* level.

Looking ahead, our next step is to take the peptides that perform best simultaneously on both fronts - strong docking affinity and favorable ADMET profile and visualize their predicted binding poses at the molecular level. This will let us actually inspect how each candidate peptide sits within the ACE and DPP-IV binding pockets, confirm which specific interactions such as hydrogen bonds, hydrophobic contacts, and so on — are driving the predicted affinity, and sanity-check that the docking scores reflect a chemically plausible, stable binding mode rather than an artifact of the scoring function. That visualization step is planned as direct follow-up work to this presentation.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx (6)" src="https://github.com/user-attachments/assets/c1f3dc94-151f-4b7b-a7c9-53714d020493" />

## Conclusions

First, *Lupinus albus* conglutins, like their better-studied counterpart *L. angustifolius*, appear to be a promising source of dual-acting ACE-I and DPP-IV inhibitory peptides. Out of 205 hydrolysis-derived candidates, 71 combined favorable ADMET profiles with strong predicted binding to at least one target, with a substantial subset — 34 peptides — active against both.

Second, we want to be explicit about the limitations of this work, and there are two I’d like to highlight beyond what I’ve already mentioned. The first concerns gastrointestinal digestion stability. Several prior *in silico* studies in this space, including some of the reference literature our methodology draws from, do not clearly specify which pepsin activity condition, or which precise pH and concentration parameters, were used in their simulated digestion step. This might seem like a minor methodological detail, but it isn’t — pepsin activity varies substantially with pH, and an under-specified or overly permissive simulation could easily generate false positives: peptides that look like excellent target inhibitors on paper, but that would, in reality, be degraded or never survive intact through actual gastrointestinal digestion. So any future gastrointestinal digestion stability analysis on our candidate peptides needs to be approached cautiously, with explicitly documented and justified enzyme activity parameters, precisely to avoid this kind of misleading result.

The second limitation, and I think the most important one to end on, is this: every result I’ve presented today, without exception, is a computational prediction. *In silico* docking scores, ADMET predictions, and hydrolysis simulations are valuable and efficient tools for narrowing an enormous search space down to a manageable, prioritized shortlist — but they are not a substitute for experimental confirmation. Every one of these candidate peptides ultimately requires wet lab validation: actual peptide synthesis, *in vitro* enzyme inhibition assays against real ACE and DPP-IV, and ideally digestion stability testing under well-characterized, properly documented conditions, before any of these peptides can be seriously considered as functional food or nutraceutical candidates.

<img width="960" height="540" alt="Stets_Havryliak_Health_Intelligence_conference pptx (7)" src="https://github.com/user-attachments/assets/48d9078b-49ba-45e4-b396-8e6827555bc0" />

## Table 1
Overall quantity of conglutin-derived peptides with specific bioactivities

<img width="346" height="512" alt="unnamed" src="https://github.com/maksymstets/lupinus/blob/main/images_results/peptide_table.png" />

## Folders and files description

| Directory       | Purpose                       | Key Contents                                            |
| --------------- | ------------------------------| ------------------------------------------------------- |
| ADMET_inputs    | Peptides for ADMET analysis   | optimised_peptides_for_admet_metadata.csv               |
| ADMET_results   | Results of an ADMET analysis  | predictions.csv, optimal_admet_activity_all_length.csv  |
| ADMET_src         Scripts for ADMET analysis      analyse_admet_activity.py, smiles_converter_metadata.py, ADMET-AI terminal commands
| BIOPEP_src   
| Docking_src
| dfs_images_src
| images_results
| inputs_fasta
| ACE ChimeraX commands and terminal meeko script
| ACE_clean.pdb
| ACE_prepared.pdbqt
| DPP IV ChimeraX commands and terminal meeko script
| DPP4_clean.pdb
| DPP4_prepared.pdbqt
| README.md
| config_ACE.txt
| config_DPP.txt
| run_all_docking.sh
| uniprotkb_accession_A0A6A4QEF0_OR_access_2026_05_29.fasta

