# Metal Gear Solid Codec Bots

*Several twitter accounts that run through transcripts of Metal Gear Solid codec conversations with each other*

Currently the bots are running through [a transcription of Metal Gear Solid 3 codec 
conversations](http://www.gamefaqs.com/ps2/914828-metal-gear-solid-3-snake-eater/faqs/43456). Every several hours the 
script will parse the transcript for the next conversation between characters. It will then step through the conversation 
every 5-10 minutes until there aren't any lines left.

**Dependencies**
 * [Twitter](https://dev.twitter.com/) consumer keys and access tokens
 * [python-twitter Module](https://github.com/bear/python-twitter)

**TODO**
 * Allow for more graceful restart

#### [Current Bot List](https://twitter.com/amarriner/lists/metal-gear-codec-bots)
 * [Major Zero](https://twitter.com/MajorZero140_85)
 * [Snake](https://twitter.com/Snake120_85)
 * [EVA](https://twitter.com/EVA_142_52)
 * [The Boss](https://twitter.com/TheBoss141_80)
 * [Sigint](https://twitter.com/Sigint148_41)
 * [Para-Medic](https://twitter.com/ParaMedic145_73)

#### Sample Tweet

<blockquote class="twitter-tweet" lang="en">
   <p>
      <a href="https://twitter.com/Snake120_85">@Snake120_85</a> Sokolov should be at the abandoned factory to the north, 
      so head in that direction.
   </p>

   &mdash; Major Zero 140.85 (@MajorZero140_85) 
   <a href="https://twitter.com/MajorZero140_85/statuses/446562976896913408">March 20, 2014</a>
</blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
