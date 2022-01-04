
protected void configure(HttpSecurity http) throws Exception {
  http.authorizeRequests()
    .antMatchers("/resources/**", "/signup", "/about").permitAll() // Compliant
    .antMatchers("/admin/**").hasRole("ADMIN")
    .antMatchers("/admin/login").permitAll() // Noncompliant; the pattern "/admin/login" should occurs before "/admin/**"
    .antMatchers("/**", "/home").permitAll()
    .antMatchers("/db/**").access("hasRole('ADMIN') and hasRole('DBA')") // Noncompliant; the pattern "/db/**" should occurs before "/**"
    .and().formLogin().loginPage("/login").permitAll().and().logout().permitAll();
}

SecureRandom sr = new SecureRandom();
sr.setSeed(123456L); // Noncompliant
int v = sr.next(32);

sr = new SecureRandom("abcdefghijklmnop".getBytes("us-ascii")); // Noncompliant
v = sr.next(32);


public class test {

  public static void main(String[] args) {
    try
    {
      Cipher c1 = Cipher.getInstance("DES"); // Noncompliant: DES works with 56-bit keys allow attacks via exhaustive search
      Cipher c7 = Cipher.getInstance("DESede"); // Noncompliant: Triple DES is vulnerable to meet-in-the-middle attack
      Cipher c13 = Cipher.getInstance("RC2"); // Noncompliant: RC2 is vulnerable to a related-key attack
      Cipher c19 = Cipher.getInstance("RC4"); // Noncompliant: vulnerable to several attacks (see https://en.wikipedia.org/wiki/RC4#Security)
      Cipher c25 = Cipher.getInstance("Blowfish"); // Noncompliant: Blowfish use a 64-bit block size makes it vulnerable to birthday attacks

      NullCipher nc = new NullCipher(); // Noncompliant: the NullCipher class provides an "identity cipher" one that does not transform or encrypt the plaintext in any way.
    }
    catch(NoSuchAlgorithmException|NoSuchPaddingException e)
    {
    }
  }
}
