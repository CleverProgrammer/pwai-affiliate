import streamlit as st
import requests

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session state
if 'form_submitted' not in st.session_state:
  st.session_state.form_submitted = False


def notify_signup_via_text(name, email, phone, num_referrals, earnings):
  api_token = st.secrets["SIMPLE_TEXTING_API"]
  account_phone_number = st.secrets["SIMPLE_TEXTING_PHONE"]
  your_phone_number = st.secrets["QAZI_PHONE"]

  message = f"New affiliate sign-up: \nName: {name}\nEmail: {email}\nPhone: {phone}\nExpected Referrals: {num_referrals}\nExpected Earnings: ${int(earnings):,}"

  url = "https://app2.simpletexting.com/v1/send"

  payload = {
      "token": api_token,
      "phone": your_phone_number,
      "from": account_phone_number,
      "message": message
  }

  response = requests.post(url, data=payload)

  if response.status_code == 200:
    print("Text message sent successfully!")
  else:
    print(
        f"Failed to send text message. Status Code: {response.status_code}, Error: {response}"
    )


def calculate_earnings(num_referrals, commission_rate, course_price):
  return num_referrals * (course_price * commission_rate / 100)


# Thank You Page
if st.session_state.form_submitted:
  st.title("WAIT. You have one IMPORTANT step left...")
  st.subheader("Click here to sign up for the referral program.")
  st.markdown(
      "[Sign up here](https://cleverprogrammer.thrivecart.com/profit-with-ai-chatgpt/partner/)"
  )
  st.write(
      "The form on the previous page was just to get your info so someone from team CP can hit you up in next few days. You still need to sign up for the affiliate program above."
  )
  st.image(
      'https://senja-io.s3.us-west-1.amazonaws.com/public/media/XwObwY6NDx9Z90Vr.png'
  )
  # # Senja Embed at the bottom
  # st.markdown("""
  #     <div class="senja-embed" data-id="93f6bab8-6901-4d67-bb60-c1d4ea231ee5" data-lazyload="false"></div>
  #     <script async type="text/javascript" src="https://static.senja.io/dist/platform.js"></script>
  #     """,
  #             unsafe_allow_html=True)

else:
  # Initial layout
  st.title("Do you want to make money sharing my course?")
  st.subheader(
      "Earn 50% commission on each student that enrolls in the course... Without limits."
  )

  st.image("https://i.imgur.com/fUS1mcS.png")

  st.write("""
    For example, if the course is priced at \$300... You'll make \$150 on each student enrolling.

    If you genuinely love the course and think your friends or family will get benefit from this... Get this course in their hands ASAP.

    If you refer 7 paying customers... That's $1,000 ;).
    """)

  # Slider
  st.markdown('## Want to see how much money you can make? Try this referral calculator here (just slide)')
  num_referrals = st.slider("How many referrals do you expect?", 0, 100, 7)

  # Constants
  COMMISSION_RATE = 50  # 50% commission rate
  COURSE_PRICE = 300  # Course price in dollars

  # Earnings Calculation
  earnings = calculate_earnings(num_referrals, COMMISSION_RATE, COURSE_PRICE)
  st.markdown(f"# Earnings 👉 ${int(earnings):,}")
  st.markdown(f"### ...on referring {num_referrals} students ❤️")
  st.markdown('')
  st.markdown('## Sign up below 👇')

  # Form for user details
  with st.form(key='signup_form'):
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    phone = st.text_input("Phone:")
    submit_button = st.form_submit_button(
        label='Yes, I Want to Join this Referral Program!')

  # On form submission
  if submit_button:
    if all([name, phone, email]):
      st.session_state.form_submitted = True
      notify_signup_via_text(name, email, phone, num_referrals, earnings)
      st.rerun()  # Force a rerun to update the page
