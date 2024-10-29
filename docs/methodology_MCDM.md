# Multi-Criteria Decision Analysis (MCDA)
Also known as Multi-Criteria Decision Making (MCDM).
Applied in `code/mcdm_analysis.ipynb`.

## What is MCDA?
Multi-Criteria Decision Analysis (MCDA or MCDM) is an approach to solving **decision-making problems**. 
It dates back to the 1950s and has been increasingly adopted in several fields, the main being: engineering, energy, 
environmental sciences and computer science. 
It emerges as a complementary tool to the inherent limitations of the human information processing system: 
a limited span of working memory; limited exactness in quantitative measurements; and human errors and contradictions (Dhurkari, 2022).  
Furthermore, MCDM can help in crucial issues related to *resource planning and management* [...] where there are many conflicting criteria to be considered, 
the parameters are liquid and there is a high degree of uncertainty of the decision impacts (Spyridakos, 2023, p. v). 

This method considers different **qualitative and quantitative criteria** that need to be fixed to find the **best solution** (Taherdoost e Madanchian, 2023, p. 77). 
Among the various methods/models available, no single method is perfect and cannot be considered suitable for use in every decision-making situation or for solving every decision problem (Sałabun et al., 2020, p. 2). 
Different methods are likely to produce different results. Choosing a suitable method for a specific problem is in itself challenging.

## The decision-making problem
In short, a decision-making problem consists of a set of **alternatives** *A* (finite or infinite) that are evaluated based on a set of **criteria** *C*. 
Usually, each i-th criteria is assigned a **weight** $w_i$ based on its importance for the result. 
This information is represented in a matrix called the **decision matrix** (*M*). 

Example of types of decisions: choice, ranking, sorting problems.

Most MCDM methods consist of the following steps: creation of decision matrix (with alternatives and criteria), 
normalization of decision matrix, weight multiplication, computation of ranking/best alternative. 

## MCDA Methods Classification
There are dozens of MCDA methods that differ on various aspects: from the type of decision problem, normalization technique, 
output produced, evaluation rules, etc. In short, we can consider the following classification reported by Taherdoost & Madanchian (2023):

1st level distinction: number of alternatives (MADM vs MODM)
- **Multi-Objective Decision Making (MODM)**: focuses on *continuous* decision spaces with an infinite number of alternatives and is also known as continuous problems of decision making → *optimization* problem.
- **Multi-Attribute Decision Making (MADM)**: *discrete* problem and concentrates on problems with explicitly known decision alternatives with finite numbers. →  *evaluation* problem (chooses the solution between a discrete number of alternatives).

2nd level of classification: operational approach (European vs American schools)
- **American school** → *functional* approach: strongly connected with the operational approach using a single synthesized criterion (as output),
  strong value of the usability of said criterion. (e.g. TOPSIS, VIKOR, COPRAS)
- **European school** → *relational* model: synthesis of criteria based on the relation of outranking.
  This relation is characterized by transgression between pairs of decision options. (e.g. PROMETHEE)

3rd level of classification: aggregation technique to assess criteria
- outranking relations (binary)
- utility function (all criteria)
- discriminant function (all criteria, linear)
- function-free (decision rule)

Then, within each method there are some *degrees of freedom*, for instance: normalization technique, weighing technique.

## MCDA for analysis of mountain huts / alpine environment
There is few research that applied MCDM to mountain huts (table), but there is a vast number of studies using such methods 
for landscape analysis, site selection, risk evaluation in the alpine environment. 

|reference|area|notes|
|---|---|---|
|Stubelj Ars, M., & Bohanec, M. (2010). Towards the ecotourism: A decision support model for the assessment of sustainability of mountain huts in the Alps. Journal of Environmental Management, 91(12), 2554–2564. https://doi.org/10.1016/j.jenvman.2010.07.006 |Slovenian Alps|Qualitative multi-criteria decision framework for evaluating mountain huts environmental  sustainability.|
|Mila Gandino. (2014). Il contributo dell’analisi multicriteri spaziale nella gestione sostenibile della rete di rifugi del CAI: il caso della provincia di Sondrio. Politecnico di Milano. Oppio, A., & Bottero, M. (2018). A strategic management based on multicriteria decision analysis: An application for the Alpine regions. International Journal of Multicriteria Decision Making, 7(3–4), 236–262. https://doi.org/10.1504/IJMCDM.2018.094384|Sondrio province (Italy)|Uses PROMETHEE II to define financial funds allocation for renovations/valorization of mountain huts. |
|Xu, Ming, Chunjing Bai, Lei Shi, Adis Puška, Anđelka Štilić, e Željko Stević. «Assessment of Mountain Tourism Sustainability Using Integrated Fuzzy MCDM Model». Sustainability 15 (28 settembre 2023): 14358. https://doi.org/10.3390/su151914358|Bosnia-Erzegovina|Fuzzy MDCM analysis (fuzzy CRADIS)  to assess sustainable tourism in 6 mountain lodges in Bosnia-Erzegovina.|

My analysis tackles a **ranking problem**, with a finite number of alternatives (mountain huts) and criteria (indicators about water, energy, etc.). 
The aim is to obtain a ranking of the huts computed using the criteria, based on the preferences in terms of environmental sustainability and self-sufficiency. 

Steps:
- identify alternatives and **criteria** to evaluate them
- choose appropriate **model(s)** for the decision problem (ranking)
- define the **weights** → literature, survey on hut’s needs, experts opinion
- apply the model to obtain **rankings**
- **evaluate** results: compare between methods & *sensitivity analysis* for weights

### Alternatives & criteria
33 alternatives (SAT’s mountain huts). [Qualitative and quantitative criteria](https://docs.google.com/drawings/d/1eFwH94PPxf7UthArq_mfeHBxfTvM_MuycQnrXQJuNbQ/edit?usp=sharing) for several categories: resources (water, energy), logistics (supplies) and social (accessibility, hospitality). 

Note! Qualitative criteria need to be converted to quantitative using a scoring system. Inspiration can be taken from similar work by Gandino (2014).

#### Scoring system (qualitative criteria)
|criteria|dtype|conversion|
|---|---|---|
|Type of water source|string|Score based on *reliability*. From least to most reliable: nosource (0), fusion (glacier/snow) (1), lake/river (2), spring (3), public water (4).|
|Type of energy source|list of strings|Score based on environmental *sustainability*. From least to most sustainable: gpl and/or (co)generator (1), public electricity (2), renewables (photovoltaic, solar-thermal, hydroelectric) (3). Final score is the mean of all sources for the hut.|
|Type of heating|string|Score based on environmental sustainability. From least to most sustainable: gas (1), renewable_option* (2), electric (3), public_electricity (4). |
|||*renewable_option: huts that did not have heating data, checked if they have a renewable source in their energy sources (which may be used for heating).|
|Mode of supplying|list of strings|Score based on environmental sustainability. From least to most sustainable: helicopter (1), vehicle (2), foot or aerialway (3). Final score is the mean of all modes for the hut (same as energy sources).|
|Type of accesses|list of strings|Score based on *difficulty* of access. From easier to harder access: public road (1), lift within 500m (2), lift within 2300m (3), hiking trails (4). Final score is the mean of all accesses for the hut (same as above).|
|Remoteness|string|CAI-SAT system for classifying huts measuring remoteness both in terms of hut supplying and for visitors. Category ‘A’ is the least remote, category ‘E’ the most. Transformed from 1 (A) to 5 (E).|

### Models
By the literature review of MCDM methods, candidate models to adopt are:

American school:
- **TOPSIS**: introduced by Hwang & Yoon (1981). Produces a ranking based on a synthesized index (score from 0 to 1). The ranking is computed according to the closeness score to ideal and distance to anti-ideal. So in this case the preference function to be chosen is the type of distance (Euclidean, Manhattan, etc.) → output: preference score, where a higher score means a better alternative. 
- **VIKOR**: introduced by Opricovic (1998). Similar to TOPSIS, produces a ranking based on the closeness score (positive values) to the best option. Uses Euclidean distance. → output: preference score, where a lower score means a better alternative. 
- **COPRAS**: introduced by Zavadskas et al (1994). Applies stepwise sorting and utility degree calculation which helps when there are conflicting criteria. → output: preference score, where a higher score means a better alternative. 

European school:
- **PROMETHEE II**: introduced by  Brans et al (2005), based on pairwise comparison (outranking). For each criterion weights and a preference function are defined. The preference function for the i-th criterion is computed for each alternative and the weighted sum over all criteria defines the aggregated preference index of alternative a over alternative b. Using outranking flows it is possible to obtain a partial ranking (PROMETHEE I) or a complete ranking (PROMETHEE II) based on such pairwise preference/dominance relations. 
PROMETHEE II was used by Gandino (2014). 

More details and comparison of these models: Zlaugotne et al. (2020); Sałabun et al, (2020). 

### Weights
The models above can be tested by using several standard approaches (equal weights, entropy, standard deviation). Another option is to assign custom weights based on literature, context and experts’ opinion. 

#### Example of custom weights (must sum up to 1)
Insights:
from Analisi delle esigenze dei rifugi alpini (2022): water and energy management are the top-two high-priority areas for the majority of hut keepers.

||criteria|weight|
|---|---|---|
|C1|water source|0.15|
|C2|water storage capacity|0.10|
|C3|energy source|0.15|
|C4|number of energy sources|0.05|
|C5|power storage capacity|0.05|
|C6|heating source|0.05|
|C7|supply mode|0.15|
|C8|types of access|0.05|
|C9|number of accesses|0.05|
|C10|remoteness|0.15|
|C11|overnight capacity|0.05|
|C12|seasonal overnight stays|0.05|




## References
Brans, J.-P., Mareschal, B., Figueira, J., Greco, S., & Ehrogott, M. (2005). Promethee Methods. https://doi.org/10.1007/0-387-23081-5_5

Dhurkari, R. K. (2022). MCDM methods: Practical difficulties and future directions for improvement. RAIRO - Operations Research, 56(4), 2221–2233. https://doi.org/10.1051/ro/2022060

Hwang, C.-L., & Yoon, K. (1981). Multiple Attribute Decision Making. Berlin, Heidelberg: Springer. https://doi.org/10.1007/978-3-642-48318-9

Mila Gandino. (2014). Il contributo dell’analisi multicriteri spaziale nella gestione sostenibile della rete di rifugi del CAI: il caso della provincia di Sondrio. Politecnico di Milano.

Opricovic, S. (1998). Multicriteria optimization of civil engineering systems. Faculty of civil engineering, Belgrade, 2(1), 5-21.

Oppio, A., & Bottero, M. (2018). A strategic management based on multicriteria decision analysis: An application for the Alpine regions. International Journal of Multicriteria Decision Making, 7(3–4), 236–262. https://doi.org/10.1504/IJMCDM.2018.094384

Sałabun, W., Wątróbski, J., & Shekhovtsov, A. (2020). Are MCDA Methods Benchmarkable? A Comparative Study of TOPSIS, VIKOR, COPRAS, and PROMETHEE II Methods. Symmetry, 12(9), 1549. https://doi.org/10.3390/sym12091549

Servizio turismo e sport. (2022). Analisi delle esigenze dei rifugi alpini. Provincia Autonoma di Trento. Retrieved from Provincia Autonoma di Trento website: https://www.provincia.tn.it/News/Approfondimenti/Analisi-delle-esigenze-dei-rifugi-alpini

Spyridakos, A. (Ed.). (2023). Multicriteria Decision Aid and Resource Management: Recent Research, Methods and Applications. Cham: Springer International Publishing. https://doi.org/10.1007/978-3-031-34892-1

Stubelj Ars, M., & Bohanec, M. (2010). Towards the ecotourism: A decision support model for the assessment of sustainability of mountain huts in the Alps. Journal of Environmental Management, 91(12), 2554–2564. https://doi.org/10.1016/j.jenvman.2010.07.006

Taherdoost, H., & Madanchian, M. (2023). Multi-Criteria Decision Making (MCDM) Methods and Concepts. Encyclopedia, 3(1), 77–87. https://doi.org/10.3390/encyclopedia3010006

Xu, Ming, Chunjing Bai, Lei Shi, Adis Puška, Anđelka Štilić, e Željko Stević. «Assessment of Mountain Tourism Sustainability Using Integrated Fuzzy MCDM Model». Sustainability 15 (28 settembre 2023): 14358. https://doi.org/10.3390/su151914358

Zavadskas, E., Kaklauskas, A., & Šarka, V. (1994). The new method of multicriteria complex proportional assessment of projects. Technological and Economic Development of Economy, 1, 131–139.

Zlaugotne, B., Zihare, L., Balode, L., Kalnbaļķīte, A., Khabdullin, A., & Blumberga, D. (2020). Multi-Criteria Decision Analysis Methods Comparison. Environmental and Climate Technologies, 24, 454–471. https://doi.org/10.2478/rtuect-2020-0028
