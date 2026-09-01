# Director Agent before/after: repair the earliest dramatic break

This is an original, public, author-run example. It demonstrates one `director-agent` diagnosis-and-revision pass. It is not an external-user case, an independent cold read, or proof that the Skill is stable in practice.

## Deliberately weak input

```screenplay
INT. EMPTY APARTMENT - EVENING

MARA looks at a bare patch on the kitchen wall.

MARA
Where's the clock?

JOEL
I don't know.

MARA
It's important to me.

JOEL
Things happened. You weren't here.

MARA
Tell me the truth.

JOEL
You wouldn't understand.

They look at each other, both hurt by the past.
```

## Diagnosis

### Earliest break

The scene has no concrete dramatic transaction. Mara says the clock is important, but the script does not establish what she needs to accomplish now, why delay matters, what Joel can grant or withhold, or what either person does when a tactic fails.

### Downstream damage

- Joel's refusal is arbitrary because he has no independent risk or protection behavior.
- “You weren't here” names backstory but does not change either person's next option.
- The dialogue is symmetrical: statement, refusal, demand, refusal.
- The clock is emotional decoration rather than a causal object.
- No exit state changes, so no next scene is forced.

## Upstream repair

- **Mara's immediate result:** recover their mother's carriage clock before its pawn ticket expires at 7:00 p.m.
- **Why now:** the pawn shop transfers expired items at closing; the apartment handover happens at the same time.
- **Joel's opposition:** he pawned the clock to cover their mother's final pharmacy bill and concealed it to protect his pride.
- **Obvious alternatives tested on the page:** call the shop, ask for a hold, drive there herself, or delay the apartment handover.
- **Why the split is necessary:** the shop refuses a hold; Mara is the named tenant required for the handover; Joel can reach the shop only if Mara gives him the redemption money and her car.
- **Concrete cost:** Mara must trust the brother who sold the clock without telling her; Joel must admit what he did and return with the object and remaining cash.

## Revised screenplay

```screenplay
INT. MOTHER'S APARTMENT - KITCHEN - 6:38 P.M.

The apartment is nearly empty. A pale square marks the wall above the sink.

MARA, 33, closes a dish box and reaches for the tape. JOEL, 28, gets there first. He tapes the box too quickly, trapping one flap crooked.

MARA
Where's the clock?

JOEL
Packed it.

Mara opens the dish box. Plates. Towels. No clock.

JOEL (CONT'D)
Maybe the bedroom one.

She takes the tape from him. A folded pawn receipt is stuck to the bottom of the roll.

Mara reads it. Joel keeps both hands on the crooked box.

MARA
It expires tonight.

JOEL
I know what it says.

Mara calls the number on the receipt and puts the phone on speaker.

PAWNBROKER (V.O.)
No holds after seven. Ticket expires, it moves to inventory.

MARA
I'm twenty minutes away.

PAWNBROKER (V.O.)
Then don't take twenty-one.

The call ends.

Mara opens her banking app. Joel watches the empty wall instead.

MARA
Why this clock?

JOEL
It was worth something.

MARA
The pharmacy was paid.

JOEL
The first week was.

Her phone buzzes: BUILDING MANAGER — “Lobby at 6:50. Handover at 7. Named tenant must sign.”

MARA
You could've called me.

JOEL
I did.

MARA
You asked for rent.

JOEL
You sent it.

MARA
Because you said rent.

Joel presses down on the box. The trapped flap pops up again.

JOEL
You were already paying that. I picked something I could fix.

Mara looks from the handover message to the pawn receipt.

MARA
How much?

JOEL
Two eighty, with the fee.

She takes three hundred dollars from an envelope marked MOVERS. Then she removes her car key from the ring.

Joel reaches for the money. Mara keeps hold of it.

MARA
Clock on the back seat. Face up.

JOEL
I know how to carry a clock.

MARA
Then bring me the change.

He meets her eyes. She lets go of the money and the key.

Joel leaves. Mara retapes the crooked box.


EXT. APARTMENT BUILDING - CURB - 7:08 P.M.

The building manager locks the front door behind Mara and walks away with the keys. Mara holds the deposit check and the last box.

Her car turns the corner.

Joel parks badly, jumps out, and opens the back door. The carriage clock lies face up in a nest of pawn-shop newspaper. Its brass case is dull but intact.

He gives Mara the car key, then seventeen dollars and some coins.

JOEL
Fee went up.

Mara counts once. She stops with the coins in her palm.

MARA
Did she know you sold it?

JOEL
She knew about the medicine.

MARA
That's not what I asked.

Joel lifts the clock out with both hands.

JOEL
She stopped asking after the second time I called you.

Mara looks at him, then at the last box by her feet.

She opens the trunk.

MARA
Clock in first.

Joel sets it down carefully. Mara wedges a folded moving blanket around it.

She picks up one end of the last box. After a beat, Joel takes the other.

They lift together.
```

## Self-audit only

| Check | Result |
|---|---|
| Plain-language causal story | Mara discovers the pawn receipt, tests the direct alternative, chooses to trust Joel with money and transport, and recovers the clock before the apartment closes |
| Scene 1 exit state | Joel has admitted the pawn and left with money/key; Mara must complete the handover alone |
| Scene 2 inheritance | The handover is complete; Joel's return proves or breaks the new trust |
| Obvious alternatives | Calling, holding the item, driving herself, and delaying handover are addressed in the scene |
| Supporting-character agency | Joel protects pride, chooses partial truth, then returns the object and change |
| Dialogue response chain | Consequential lines answer a receipt, call, message, prior wording, money handoff, or returned object |
| Prop function | Receipt changes knowledge; money/key change options; clock recovery changes the physical result |
| Anti-neatness pass | The siblings do not fully reconcile or explain the theme; they resume a shared physical task |

No independent cold reader was used. This record is therefore **SELF-AUDIT ONLY**. It demonstrates a bounded author-run forward test and remains open to external critique in the [Showcase discussion](https://github.com/62656456/ai-film-skills/discussions/7).
