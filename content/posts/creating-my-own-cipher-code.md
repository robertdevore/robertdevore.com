---
title: "Creating my own cipher code"
description: "I can’t remember what sparked the idea, but I got bit by a strong urge to create my own cipher. Maybe it’s all the spy shit I watch on TV 😂 Regardless, I knew that there were a couple of things that I needed to figure…"
custom_url: "creating-my-own-cipher-code"
author: "Robert DeVore"
date: "2022-11-28"
canonical: "https://robertdevore.com/creating-my-own-cipher-code/"
template: "signal-c"
nav_hide: true
excerpt: "I can’t remember what sparked the idea, but I got bit by a strong urge to create my own cipher. Maybe it’s all the spy shit I watch on TV 😂 Regardless, I knew that there were a couple of things that I needed to figure…"
categories: ["Developer Tools"]
tags: ["Engineering"]
---

I can’t remember what sparked the idea, but I got bit by a strong urge to create my own cipher.

Maybe it’s all the spy shit I watch on TV 😂

Regardless, I knew that there were a couple of things that I needed to figure out in order to build my own custom cipher system.

  1. A way to create randomized code
  2. A way to encrypt the hidden message
  3. A way to decrypt the hidden message



So I thought about it for a while and then I came up with something relatively simple.

> ==== Begin Cipher ====
> 
> ohiylokhbianllegheeeguonanqdkiloynobkemmwgounjunlwhcrenaiamsoeakolwulkhuhuuktiamwtolhuuakafwobizenelufakkewbuehuepzkneyauwgktuhnioakefenulldwqeeiuamoolwlhaowtmealazngaaahnngubwaown
> 
> ==== End Cipher ====

Can you crack it?

Hint: There’s a quote that has each word’s characters scrambled, and then in-between each scrambled word is a letter.

Those extra letters are what the secret message is. The message is translated from it’s English origin to Zulu.

First, figure out the quote, then figure out the message.

**My thoughts behind this setup:**

The quotes used should be changed out with each communication and the language translation can also be switched.

So without knowing the language used and the quote that’s being randomized, it’d be hard for a random person to decipher.

## Example Use Case:

Steve and Anna need to communicate privately. 

They decide on Dutch as the translated language. 

They settle on [“Anarchism and other Essays” by Emma Goldman](https://theanarchistlibrary.org/library/emma-goldman-anarchism-and-other-essays)

  * Message 1 = from Chapter 1
  * Message 2 = from Chapter 2
  * … until finished



Here is an example with the first sentence of chapter 1, in Dutch with characters from each word randomized.

> ==== Begin Cipher ====
> 
> desndgsceeiehinavemknjeseliieogrnegitinwlknkeosigtilieejjedtrkdecegehdiesnsinavedsrekkrjelikcevihjdrsitavnlekuewinideetdadeednraginvnaeenrerldheeedeaaarddgtidnuli
> 
> ==== End Cipher ====

Now if you know the words used and language used, you can figure out the letter count of each word.

Letter counts: 2, 12, 3, 10, 5, 2, etc… 

For Steve to add the hidden text, he would add each letter of the message directly after each of those letter counts.

> ==== Begin Cipher ====
> 
> de**h** sndgsceeiehi**e** nav**l** emknjeseli**l** ie**o** grlnegitinwlknkeosigtilieejjedtrkdecegehdiesnsinavedsrekkrjelikcevihjdrsitavnlekuewinideetdadeednraginvnaeenrerldheeedeaaarddgtidnuli
> 
> ==== End Cipher ====

Using the letter count mentioned, we can see that the hidden message says “hello” (highlighted in the text above)

## Taking it further

I put together a code example of how this may work in PHP to programmatically create the cipher and expand on its use.

For example, what if we wanted to make the lowercase text blocks less readable to the naked eye?

There’s a couple of things that can be done:

  * Capitalize random letters
  * Insert random symbols between words



When we randomly add symbols into the cipher, it ends up looking even more like gibberish:

> ==== Begin Cipher ====
> 
> cadiied,ecaad?malvaapr>+,gebsaralhamod=+ee&enetr+$caad#${rapalav]redbaaaalhm;h=*a*gsenemma<=`ratcees=+[a[samegemn-)&izuraadtd}de&]asu*+ogmeri=;laeigns{paar-+}uulz/rorepimi.}reasudcb$a=?[icota&!?
> 
> ==== End Cipher ====

And when we add capitalization into the mix, this text block is even more unreadable than the previous:

> ==== Begin Cipher ====
> 
> PtKnuueJ*{aTAaDPrTe=-?nipkENta~sYnaG!.%sYuAMIEpmn/HSKAAAr#!>EapSTEi??ERAakPeaNt_)$Iygna>=%eckDAaI-<,DnDA~%MaiEUkNDm#%[#GdI](https://twitter.com/search?q=%23GdI).-+araAnt;sIApTe:rnPakAeAT&AnGY#>diAcak(-.lAHAi`.aSuT[uFrhu+TUSRSUataR-:[TAHmAbna([uit/aADAlh+SeMJE?/AIasHr.=MESe
> 
> ==== End Cipher ====

**Download the code**

The code for the PHP functions along with example usage can be [found on GitHub](https://gist.github.com/robertdevore/8bba7aef2f98f64f05878c15753aa9f3).

### Embedded in an image?

So now that we’ve got the message encryption set up, how do we share these messages with others that we need to communicate with?

One way would be to embed the created cipher into an image that can then be shared online.

An example a before/after image can be found in the following tweet from when I live-tweeted the whole idea for this cipher.

> I can now add "add the cipher to an image file" to the mix 👀  
>   
> Find a corner of the internet to communicate through, add your message to an image and post it.  
>   
> Open these images in your fav text editor to find message  
>   
> I think I may have finally found a reason to use [@Tumblr](https://twitter.com/tumblr?ref_src=twsrc%5Etfw) 🤷😂 [pic.twitter.com/X0sGSU0vbG](https://t.co/X0sGSU0vbG)
> 
> — Robert DeVore (@deviorobert) [June 27, 2022](https://twitter.com/deviorobert/status/1541277175298547712?ref_src=twsrc%5Etfw)

It's not fool proof, and since I've tweeted **AND** blogged about it, you should consider this setup burned. This was simply created because I wanted to have some fun, and I did 🤘 Itch, scratched.

## Related Reading

- [Zero Cool CLI – A Hacker’s Terminal from 1995](/zero-cool-cli-a-hackers-terminal-from-1995/)
- [Complete Beginner’s Guide: Building a Python URL Checker for Google Sheets](/complete-beginners-guide-building-a-python-url-checker-for-google-sheets/)
- [I Built a Python Stego-Cipher Tool (And You Can Have It)](/i-built-a-python-stego-cipher-tool-and-you-can-have-it/)
